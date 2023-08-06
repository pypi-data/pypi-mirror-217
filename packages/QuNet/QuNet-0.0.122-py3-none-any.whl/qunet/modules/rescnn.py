import copy
import numpy as np, matplotlib.pyplot as plt
import torch, torch.nn as nn

from ..config      import Config
from ..modelstate  import ModelState
from .total        import get_activation
from .residual     import Residual

#===============================================================================

class ConvBlock(nn.Sequential):
    def __init__(self, in_channels, out_channels, kernel_size=3, stride=1, bias=False, norm=1, fun="relu"):
        """
        Simple convolution block

        Args
        ------------        
        norm (int = 1):
            0: no, 1: BatchNorm2d, 2: InstanceNorm2d
        """
        padding = (kernel_size - 1) // 2
        layers = [nn.Conv2d(in_channels, out_channels, kernel_size, stride=stride, padding=padding, bias=bias)]

        if   norm == 1:
            layers.append(  nn.BatchNorm2d   (out_channels) )
        elif norm == 2:
            layers.append(  nn.InstanceNorm2d(out_channels) )    

        if fun: 
            layers.append( get_activation(fun) )

        super().__init__(*layers)

#===============================================================================

class ResidualConvBlock(nn.Sequential):
    def __init__(self, in_channels, out_channels, kernel_size=3,  bias=False, norm=1, num = 2,  fun="relu"):        
        """
        shape and channels will not change
        """
        padding = (kernel_size - 1) // 2        
        layers  = [] 
        for i in range(num):
            stride  = 1 if in_channels == out_channels else 2
            layers.append(nn.Conv2d(in_channels, out_channels, kernel_size, stride=stride, padding=padding, bias=bias) )
            in_channels = out_channels

            if   norm == 1:
                layers.append(  nn.BatchNorm2d   (out_channels) )
            elif norm == 2:
                layers.append(  nn.InstanceNorm2d(out_channels) )    

            if i+1 < num and fun:
                layers.append( get_activation(fun) )
                 
        super().__init__(*layers)        

#===============================================================================

class DownPoolBlock(nn.Sequential):
    def __init__(self, in_channels, out_channels, kernel_size=3,  bias=False,  norm=1, fun="relu", drop=0.):
        super().__init__(
            ConvBlock(in_channels, out_channels, kernel_size, bias=bias, norm=norm, fun=fun),
            nn.MaxPool2d(2),
            nn.Dropout2d(drop)
        )

#===============================================================================

class DownStrideBlock(nn.Sequential):
    def __init__(self, in_channels, out_channels,  bias=False,  norm=1, fun="relu", drop=0.):
        super().__init__(
            ConvBlock(in_channels, out_channels, 2, stride=2, bias=bias, norm=norm, fun=fun),            
            nn.Dropout2d(drop)
        )        

#===============================================================================

class ResCNN(nn.Module):
    def __init__(self,  *args, **kvargs) -> None:
        """
        ConvBlock: c[channels]_[kernel]_[stride] - 
            c64     - ConvBlock(..., 64, kernel_size=3, padding=1)
            c64_5   - ConvBlock(..., 64, kernel_size=5, padding=2)
            c64_7_2 - ConvBlock(..., 64, kernel_size=7, padding=3, stride=2)

        Pool2d: p[kernel]_[stride]
            p       - nn.MaxPool2d(kernel=2, stride=2)
            p3_2    - nn.MaxPool2d(kernel=3, stride=2, padding=1)

        Norm2d: n[kind] 
            n       - BatchNorm2d
            n1      - BatchNorm2d
            n2      - InstanceNorm2d

        Residual
            r      - Residual (don't change size of immage and channels)
            r128   - Residual with change number of channels like resnetXX

        DownBlock
            d128   - DownPoolBlock  (..., channels)
            s128   - DownStrideBlock(..., channels)

        Activation: (see get_activation in total.py)
            relu
            gelu, ...
            

        """
        super().__init__()
        self.cfg = ResCNN.default()
        cfg = self.cfg.set(*args, **kvargs)

        assert cfg.input is not None and type(cfg.input)==int, f"Wrong cfg.input={cfg.input}, should be int (number of input channels)"
        channels = cfg.input

        tokens = cfg.blocks.replace('(', ' ').replace(')', ' ').split(' ')                
        blocks = []
        for b in tokens:
            if len(b) == 0:
                continue

            if  b[0] == 'c' and ( len(b) == 1 or b[1].isdigit() ):        
                parts  = b[1:].split('_')                
                chan   = int(parts[0]) if len(parts) > 0 else channels
                kern   = int(parts[1]) if len(parts) > 1 else 3
                stride = int(parts[2]) if len(parts) > 2 else 1                
                conv = ConvBlock(channels, chan, kern, stride=stride,  bias=cfg.bias, norm=cfg.norm, fun=cfg.fun)                
                conv.name = b
                blocks.append( conv )
                channels = chan

            elif b[0] == 'p' and ( len(b) == 1 or b[1].isdigit() ):
                parts  = b[1:].split('_')                
                kern   = int(parts[0]) if len(parts) > 0 else 2
                stride = int(parts[1]) if len(parts) > 1 else 2                
                pad = (kern - 1) // 2
                blocks.append( nn.MaxPool2d(kernel_size=kern,stride=stride, padding=pad) )                

            elif b[0] == 'n' and ( len(b) == 1 or b[1].isdigit() ):                
                parts  = b[1:].split('_') if len(b) > 1 else ['1']
                kind   = int(parts[0]) if len(parts) > 0 else 1
                if kind == 1:
                    blocks.append( nn.BatchNorm2d   (channels) )
                else:
                    blocks.append( nn.InstanceNorm2d(channels) )

            elif b[0] == 'r' and ( len(b) == 1 or b[1].isdigit() ):        
                Eout = channels
                if len(b[1:]):                    
                    Eout = int(b[1:])
                blocks.append(  
                    Residual( 
                        ResidualConvBlock(channels, Eout, bias=cfg.bias, norm=cfg.norm, fun=cfg.fun),
                        E=channels, Eout=Eout, res = cfg.res, gamma=cfg.gamma, 
                        norm_before=0, norm_after = 0,   # подстраиваемся под resnetXX
                        norm_align = 0 if channels==Eout else cfg.norm,
                        dim=2, name=b ))         
                channels = Eout
                       
            elif  b[0] == 'd' and ( len(b) == 1 or b[1].isdigit() ):        
                parts = b[1:].split('_')
                chan = int(parts[0]) if len(parts) > 0 else channels
                block = DownPoolBlock(channels, chan, bias=cfg.bias, norm=cfg.norm, fun=cfg.fun)
                block.name = b
                blocks.append( block )
                channels = chan 

            elif b[0] == 's' and ( len(b) == 1 or b[1].isdigit() ):        
                parts = b[1:].split('_')
                chan = int(parts[0]) if len(parts) > 0 else channels
                block = DownStrideBlock(channels, chan, bias=cfg.bias, norm=cfg.norm, fun=cfg.fun)
                block.name = b
                blocks.append( block )
                channels = chan 

            else:
                assert b in ['relu', 'gelu', 'relu6', 'sigmoid', 'tanh', 'swish', 'hswish', 'hsigmoid'], f"Unknown activation function {b}"
                blocks.append( get_activation(b) )

        if cfg.pool:
            blocks.append( nn.AdaptiveAvgPool2d(1) )

        self.blocks = nn.ModuleList(blocks)

    #---------------------------------------------------------------------------

    def forward(self, x):
        """  (B,C,H,W) -> (B,C',H',W') """
        for block in self.blocks:
            x = block(x)             
        return x
    
    #---------------------------------------------------------------------------

    def update(self):
        for block in self.blocks:
            if  hasattr(block, "update"):
                block.update()

    #---------------------------------------------------------------------------

    def debug(self, value):
        for block in self.blocks:
            if  hasattr(block, "debug"):
                block.debug(value)                

    #---------------------------------------------------------------------------

    def debug(self, value=True, beta=None):
        for block in self.blocks:
            if  hasattr(block, "debug"):
                block.debug(value, beta)                

    #---------------------------------------------------------------------------

    def set_drop(self, drop=None, drop_b=None, std=None, p=None):
        num_res = sum([1 for block in self.blocks if type(block) == Residual])

        drop   = [drop]  *num_res if drop   is None or type(drop) in [int, float] else drop
        drop_b = [drop_b]*num_res if drop_b is None or type(drop_b) in [int, float] else drop_b
        std    = [std]   *num_res if std is None or type(std) in [int, float] else std
        p      = [  p]   *num_res if   p is None or type(p)   in [int, float] else p

        i=0
        for block in self.blocks:
            if type(block) == Residual:
                block.set_drop(drop[i], drop_b[i], std[i], p[i])
                i += 1

    #---------------------------------------------------------------------------

    @staticmethod
    def default():
        return copy.deepcopy(Config(
            input  = 3,   
            blocks = "",
            bias   = False,
            norm   = 1,            
            fun    = 'relu',
            res    = 2,
            gamma  = 0.1,
            pool   = True,
        ))

    #---------------------------------------------------------------------------
    @staticmethod
    def resnet18():
        """resnet18 
        ```
        # Equal:
        from torchvision.models import resnet18
        model = resnet18()
        ```
        """
        cfg = ResCNN.default()
        cfg(
            input    = 3,
            blocks   = "(c64_7_2  p3_2) r r r128 r r256 r r512 r",
            norm     = 1,      
            fun      = 'relu',
            res      = 1,
            pool     = True
        )        
        return cfg

    #---------------------------------------------------------------------------

    @staticmethod
    def unit_test():
        B,C,H,W = 1, 3, 128,128
        cnn = ResCNN(input = C, blocks = "c64 d128 r d256 r r d256 r d512 r")      
        #cnn = ResCNN(ResCNN.resnet18())
        state = ModelState(cnn)                  
        state.layers(2)
        x = torch.rand(B,C,H,W)
        cnn.debug(True)
        y = cnn(x)
        y.mean().backward()
        cnn.update()
        cnn.plot()
        print(f"ok ResCNN, output = {tuple(y.shape)}")

        return True

    #---------------------------------------------------------------------------

    def plot(self, w=12, h=3, eps=1e-8, bar_width = 0.75, info=False):
        blocks = self.blocks
        idx = np.arange(len(blocks))
    
        fig, ax = plt.subplots(1,1, figsize=(w, h))
    
        ax.grid(ls=":")
        ax.set_xticks(idx)
        ax.set_yscale('log'); ax.set_ylabel("dx/x");  ax.set_xlabel("blocks");
    
        plt.text(0,0,f" std\n\n", ha='left', transform = ax.transAxes, fontsize=6, family="monospace")
                
        res = [0]*len(blocks)
        for i,block in enumerate(blocks):            
            if hasattr(block, 'sqr_dx') and block.sqr_dx is None and block.sqr_x is None:
                dx = (block.sqr_dx / (block.sqr_x+eps)).sqrt().cpu().item()
                res[i] = dx

        #ax.set_ylim(ymin=0, ymax=max(np.max(fft), np.max(att), np.max(mlp)*1.1) ) 
        
        ax.bar(idx,              res, width = bar_width, edgecolor ='grey', alpha=0.5)    
        
        ymin, ymax = ax.get_ylim()
        for i,block in enumerate(blocks):            
            if hasattr(block, 'name'):                      
                st = f"{block.std.cpu().item():.1f}" if hasattr(block, 'std') else ""
                plt.text(i, ymin, f"{st}\n{block.name}\n", ha='center', fontsize=6, family="monospace")    
    
        ax2 = ax.twinx()
        gamma_d = [0]*len(blocks)
        for i,block in enumerate(blocks):            
            if hasattr(block, 'gamma_d') and block.gamma_d is None:  
                gamma_d[i] = block.gamma_d.sqrt().cpu().item()
        ax2.plot(idx,gamma_d, marker=".")
        ax2.set_ylabel("gamma")
    
        ax3 = ax.twinx()
        ax3.set_yscale('log')
        gamma_g = [0]*len(blocks)
        for i,block in enumerate(blocks):
            if hasattr(block, 'gamma_g') and block.gamma_g is not None:  
                gamma_g[i] = block.gamma_g.sqrt().cpu().item()
        ax3.plot(idx, gamma_g, ":", marker=".")
        ax3.set_ylabel("gamma grad")
        ax3.spines["right"].set_position(("outward", 50))    
    
        plt.show()


