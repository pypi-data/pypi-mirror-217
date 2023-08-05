import copy
import numpy as np, matplotlib.pyplot as plt
import torch, torch.nn as nn

from .transformer import Residual
from ..config     import Config

"""
https://ai.stackexchange.com/questions/28326/why-class-embedding-token-is-added-to-the-visual-transformer
"""
    
#===============================================================================

class VitEmb(nn.Module):
    """    
    
    """
    def __init__(self,  *args, **kvargs) -> None:
        """ Проектор ViT из картинки в векоры патчей

        Args
        ------------
            input  (tuple=None):
                input tensor shape: (channels, height, width); 
            hidden (int = None)
                number of hidden channles
            E (int = 128):
                patch embedding dimension
            size (tuple = (8,8):
                patch height and width in px
            drop_cnn (float = 0.): 
                Dropout2d in hidden cnn
            drop_out (float = 0.):
                out Dropout
        """
        super().__init__()
        self.cfg = Config(
            input    = None,    # image (channels, height, width)
            hidden   = None,    # is hidden Conv2d
            E        = 256,     # patch embedding dimension
            size     = (8,8),   # patch (height, width)              
            drop_cnn = 0.0,     # dropout2d in hidden cnn
            drop_out = 0.0,     # out drop
        )        
        cfg = self.cfg.set(*args, **kvargs)
        
        # number of patches on y and x
        self.grid      = (cfg.input[1] // cfg.size[0],   cfg.input[2] // cfg.size[1])
        self.n_patches = self.grid[0] * self.grid[1]

        if cfg.hidden:
            self.emb = nn.Sequential(
                nn.Conv2d(cfg.input[0], cfg.hidden, 3, padding=1),
                nn.GELU(),
                nn.Dropout2d(cfg.drop_cnn),
                nn.Conv2d(cfg.hidden, cfg.E, kernel_size=cfg.size, stride=cfg.size) )
        else:
            self.emb = nn.Conv2d(cfg.input[0], cfg.E, kernel_size = cfg.size, stride=cfg.size)        

        self.pos  = nn.Parameter(torch.zeros(1, self.n_patches, cfg.E))        
        self.drop = nn.Dropout(cfg.drop_out)        

    #---------------------------------------------------------------------------

    def forward(self, x):      # (B,C,H,W)
        x = self.emb(x)        # (B,E,nx,ny)
        x = x.flatten(2)       # (B,E,P)     P = ny*nx
        x = x.transpose(1, 2)  # (B,P,E)    
        x = x + self.pos       #             position encoding
        x = self.drop(x)
        return x               # (B,P,E)

    #---------------------------------------------------------------------------

    @staticmethod
    def unit_test():
        B,C,H,W = 1, 3, 64,32
        emb = VitEmb(input=(C,H,W), pw=16, ph=8, E=128, hidden=16)
        x = torch.rand(B,C,H,W)
        y = emb(x)        
        print(f"ok VitEmb: {tuple(x.shape)} -> {tuple(y.shape)}")
        return True

#===============================================================================

class Vit2dEmb(nn.Module):
    def __init__(self,  *args, **kvargs) -> None:
        """ Проектор ViT из картинки в векоры патчей

        Args
        ------------
            input  (tuple=None):
                input tensor shape: (channels, height, width); 
            hidden (int = None)
                number of hidden channles
            E (int = 128):
                patch embedding dimension
            ph, pw (int = 16,16):
                patch size in px
            drop_cnn (float = 0.): 
                Dropout2d in hidden cnn
            drop_out (float = 0.):
                out Dropout
        """
        super().__init__()
        self.cfg = Config(
            input = None,      # image (channels, height, width)
            hidden= None,      # is hidden Conv2d
            E        = 256,    # patch embedding dimension
            ph       = 8,      # patch height
            pw       = 8,      # patch width            
            drop_cnn = 0.0,    # dropout2d in hidden cnn
            drop_out = 0.0,    # out drop
        )        
        cfg = self.cfg.set(*args, **kvargs)

        self.shape     = (cfg.input[1] // cfg.ph,   cfg.input[2] // cfg.pw)
        self.n_patches = self.shape[0] * self.shape[1]

        if cfg.hidden:
            self.proj = nn.Sequential(
                nn.Conv2d(cfg.input[0], cfg.hidden, 3, padding=1),
                nn.GELU(),
                nn.Dropout2d(cfg.drop_cnn),
                nn.Conv2d(cfg.hidden, cfg.E, kernel_size=(cfg.ph, cfg.pw), stride=(cfg.ph, cfg.pw)) )
        else:
            self.proj = nn.Conv2d(cfg.input[0], cfg.E, kernel_size=(cfg.ph, cfg.pw), stride=(cfg.ph, cfg.pw) )        

        self.pos  = nn.Parameter(torch.zeros(1, self.n_patches, cfg.E))        
        self.drop = nn.Dropout(cfg.drop_out)        

    #---------------------------------------------------------------------------

    def forward(self, x):      # (B,C,H,W)
        x = self.proj(x)       # (B,E,Py,Px)
        x = x.flatten(2)       # (B,E,P)     P = Py * Px
        x = x.transpose(1, 2)  # (B,P,E)    
        x = x + self.pos       #             position encoding
        x = self.drop(x)
        return x               # (B,P,E)

    #---------------------------------------------------------------------------

    @staticmethod
    def unit_test():
        B,C,H,W = 1, 3, 64,32
        proj = Vit2dEmb(input=(C,H,W), pw=16, ph=8, E=128, hidden=16)
        x = torch.rand(B,C,H,W)
        y = proj(x)        
        print(f"ok Vit2dEmb: {tuple(x.shape)} -> {tuple(y.shape)}")
        return True

#===============================================================================
#                                      ViT 2D
#===============================================================================


class Attention2d(nn.Module):
    """
    Attention with relative position encoding  (B,E,ny,nx) -> (B,E,ny,nx)
    https://juliusruseckas.github.io/ml/cifar10-vit.html    
    """
    def __init__(self, E, H, shape):
        """
        E - embedding; H - number of heads
        shape = (ny,nx)
        """
        super().__init__()
        self.heads = H
        self.head_channels = E // H
        self.scale = self.head_channels**-0.5
        
        self.to_keys    = nn.Conv2d(E, E, kernel_size=1)  
        self.to_queries = nn.Conv2d(E, E, kernel_size=1)
        self.to_values  = nn.Conv2d(E, E, kernel_size=1)
        self.unifyheads = nn.Conv2d(E, E, kernel_size=1)
        
        ny, nx = shape
        self.pos_enc = nn.Parameter(torch.Tensor(self.heads, (2*ny - 1) * (2*nx - 1)))
        self.register_buffer("relative_indices", self.get_indices(ny, nx))
    
    #---------------------------------------------------------------------------

    def forward(self, x):
        b, _, ny, nx = x.shape              # B,E,ny,nx
        
        keys    = self.to_keys(x).   view(b, self.heads, self.head_channels, -1)
        values  = self.to_values(x). view(b, self.heads, self.head_channels, -1)
        queries = self.to_queries(x).view(b, self.heads, self.head_channels, -1)
        
        att = keys.transpose(-2, -1) @ queries
        
        indices     = self.relative_indices.expand(self.heads, -1)
        rel_pos_enc = self.pos_enc.gather(-1, indices)
        rel_pos_enc = rel_pos_enc.unflatten(-1, (ny * nx, ny * nx))
        
        att = att * self.scale + rel_pos_enc
        att = nn.functional.softmax(att, dim=-2)
        
        out = values @ att
        out = out.view(b, -1, ny, nx)
        out = self.unifyheads(out)
        return out
    
    #---------------------------------------------------------------------------

    @staticmethod
    def get_indices(ny, nx):
        y = torch.arange(ny, dtype=torch.long)
        x = torch.arange(nx, dtype=torch.long)
        
        y1, x1, y2, x2 = torch.meshgrid(y, x, y, x, indexing='ij')
        indices = (y1 - y2 + ny - 1) * (2 * nx - 1) + x1 - x2 + nx - 1
        indices = indices.flatten()
        
        return indices
    
#===============================================================================

class MLP2d(nn.Sequential):
    def __init__(self, E, stretch=4):
        hidden_channels = E * stretch
        super().__init__(
            nn.Conv2d(E, hidden_channels, kernel_size=1),
            nn.GELU(),
            nn.Conv2d(hidden_channels, E, kernel_size=1)   
        )

#===============================================================================

class ViT2dBlock(nn.Sequential):
    def __init__(self, E, H, shape):
        super().__init__(
            Residual(                
                Attention2d(E,H, shape),                
                E = E,
                res = 2,
            ),
            Residual(                                        
                MLP2d(E),                
                E = E, 
                res = 2,
            )
        )

#===============================================================================

class Vit2d(nn.Module):
    def __init__(self,  *args, **kvargs) -> None:
        super().__init__()
        self.cfg = Vit2d.default()
        cfg = self.cfg.set(*args)

        #self.emb = 

        blocks = []
        for i in range(cfg.n_blocks):
            block = None #ViT2dBlock(E=cfg.E, E=cfg.H, shape)
            blocks.append(block)
        self.blocks= nn.ModuleList(blocks)        

 #---------------------------------------------------------------------------

    @staticmethod
    def default():
        return copy.deepcopy(Config(
            E        = None,  # embedding of patches
            H        = 1,     # number of heads
            ph       = 8,     # patch height
            pw       = 8,     # patch width                    
            n_blocks = 1,     # число слоёв трансформера
            gamma    = 0.1,   # initial value of the learning residual multiplier            
            drop     = 0.
        ))
    #---------------------------------------------------------------------------

    def forward(self, x):
        """  (B,E.H,W) -> (B,E.H,W) """
        for block in self.blocks:
            x = block(x)                           # (B,E,H,W)
        return x

    #---------------------------------------------------------------------------

    def update(self):
        for block in self.blocks:
            block.update()

    #---------------------------------------------------------------------------

    def decay(self):
        res = set()
        for block in self.blocks:
            res.update(block.decay() )    
        return res        
