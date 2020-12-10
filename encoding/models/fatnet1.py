from __future__ import division

import torch
import torch.nn as nn
import torch.nn.functional as F

from .fcn import FCNHead
from .base import BaseNet

__all__ = ['fatnet1', 'get_fatnet1']
# add 1x1 channel transform for local patch
up_kwargs = {'mode': 'bilinear', 'align_corners': True}
class fatnet1(nn.Module):
    def __init__(self, nclass, backbone, aux=True, se_loss=False, norm_layer=nn.BatchNorm2d,  base_size=520, crop_size=480, mean=[.485, .456, .406],
                 std=[.229, .224, .225], **kwargs):
        super(fatnet1, self).__init__()
        self.mean = mean
        self.std = std
        self.base_size = base_size
        self.crop_size = crop_size
        self._up_kwargs = up_kwargs

        self.base = fatnet1_base(norm_layer)
        self.head = fatnet1Head(48, nclass, norm_layer, up_kwargs=self._up_kwargs)

    def forward(self, x):
        imsize = x.size()[2:]
        x = self.base(x)
        x = self.head(x)
        x = F.interpolate(x, imsize, **self._up_kwargs)
        outputs = [x]
        return tuple(outputs)
    
    def evaluate(self, x, target=None):
        pred = self.forward(x)
        if isinstance(pred, (tuple, list)):
            pred = pred[0]
        if target is None:
            return pred
        correct, labeled = batch_pix_accuracy(pred.data, target.data)
        inter, union = batch_intersection_union(pred.data, target.data, self.nclass)
        return correct, labeled, inter, union



class fatnet1Head(nn.Module):
    def __init__(self, in_channels, out_channels, norm_layer, up_kwargs=None):
        super(fatnet1Head, self).__init__()
        self._up_kwargs = up_kwargs

        inter_channels = 512
        self.conv5 = nn.Sequential(nn.Conv2d(in_channels, inter_channels, 3, padding=1, bias=False),
                                   norm_layer(inter_channels),
                                   nn.ReLU(),
                                   )

        self.conv6 = nn.Sequential(nn.Dropout2d(0.1), nn.Conv2d(inter_channels, out_channels, 1))

    def forward(self, x):
        out = self.conv5(x)
        return self.conv6(out)

class fatnet1_base(nn.Module):
    def __init__(self, norm_layer=nn.BatchNorm2d):
        super(fatnet1_base, self).__init__()
        self.layer1 = fatnet1_layer(3,64,1,1,norm_layer)
        self.layer2 = fatnet1_layer(64,64,1,1,norm_layer)
        
        self.layer3 = fatnet1_layer(64,48,1,2,norm_layer)
        self.layer4 = fatnet1_layer(48,48,1,2,norm_layer)
        
        self.layer5 = fatnet1_layer(48,48,1,4,norm_layer)
        self.layer6 = fatnet1_layer(48,48,1,4,norm_layer)
        self.layer7 = fatnet1_layer(48,48,1,4,norm_layer)
        
        self.layer8 = fatnet1_layer(48,48,1,8,norm_layer)
        self.layer9 = fatnet1_layer(48,48,1,8,norm_layer)
        self.layer10 = fatnet1_layer(48,48,1,8,norm_layer)
        
        self.layer11 = fatnet1_layer(48,48,1,16,norm_layer)
        self.layer12 = fatnet1_layer(48,48,1,16,norm_layer)
        self.layer13 = fatnet1_layer(48,48,1,16,norm_layer)


    def forward(self, x):
        x1=self.layer1(x)
        x2=self.layer2(x1)
        
        x3=self.layer3(x2)
        x4=self.layer4(x3)
        
        x5=self.layer5(x4)
        x6=self.layer6(x5)
        x7=self.layer7(x6)
        
        x8=self.layer8(x7)
        x9=self.layer9(x8)
        x10=self.layer10(x9)
        
        x11=self.layer11(x10)
        x12=self.layer12(x11)
        x13=self.layer13(x12)
        return x13



class fatnet1_layer(nn.Module):
    def __init__(self, in_planes, out_planes, dilation=1, tl_size=1, norm_layer=nn.BatchNorm2d):
        super(fatnet1_layer, self).__init__()
        self.tl_size = tl_size
        self.inplanes = in_planes
        self.outplanes = out_planes
        self.conv = nn.Sequential(nn.Conv2d(in_planes*tl_size*tl_size, out_planes*tl_size*tl_size, 3, padding=1, dilation=1, groups=tl_size*tl_size, bias=False),
                                   norm_layer(out_planes*tl_size*tl_size), nn.ReLU())
        self.conv2 = nn.Sequential(nn.Conv2d(out_planes*tl_size*tl_size, out_planes*tl_size*tl_size//4, 1, padding=0, dilation=1, groups=1, bias=False),
                                   norm_layer(out_planes*tl_size*tl_size//4), nn.ReLU(),
                                   nn.Conv2d(out_planes*tl_size*tl_size//4, out_planes*tl_size*tl_size, 1, padding=0, dilation=1, groups=1, bias=False),
                                   norm_layer(out_planes*tl_size*tl_size), nn.ReLU())
        # self.conv_list = nn.ModuleList([nn.Sequential(nn.Conv2d(in_planes, out_planes, 3, padding=1, dilation=1, bias=False),
        #                            norm_layer(out_planes), nn.ReLU()) for i in range(tl_size^2)])

    def forward(self, x):
        x_fat = pixelshuffle_invert(x, (self.tl_size, self.tl_size))
        # x_fat_list = torch.split(x_fat, self.inplanes, dim=1)
        # out = torch.cat([self.conv_list[i](x_fat_list[i]) for i in range(self.tl_size^2)], dim=1)
        out = self.conv(x_fat)
        out = self.conv2(out)
        
        out = pixelshuffle(out, (self.tl_size, self.tl_size))
        return out


def get_fatnet1(dataset='pascal_voc', backbone='resnet50', pretrained=False,
                 root='~/.encoding/models', **kwargs):
    # infer number of classes
    from ..datasets import datasets
    model = fatnet1(datasets[dataset.lower()].NUM_CLASS, backbone=backbone, root=root, **kwargs)
    if pretrained:
        raise NotImplementedError

    return model

class ASPP_TLConv(nn.Module):
    def __init__(self, in_planes, out_planes, dilation=[1], tl_size=1):
        super(ASPP_TLConv, self).__init__()
        self.conv_list = nn.ModuleList()
        self.tl_size = tl_size
        for i in range(tl_size * tl_size):
            self.conv_list.append(
                ASPP(in_planes, out_planes, dilation, stride=tl_size)
            )

    def forward(self, x):
        out = []
        conv_id = 0
        for i in range(self.tl_size):
            for j in range(self.tl_size):
                y = F.pad(x, pad=(-j, j, -i, i))
                out.append(self.conv_list[conv_id](y))
                conv_id += 1

        outs = torch.cat(out, 1)
        outs = F.pixel_shuffle(outs, upscale_factor=self.tl_size)

        return outs
    
def pixelshuffle(x, factor_hw):
    pH = factor_hw[0]
    pW = factor_hw[1]
    y = x
    B, iC, iH, iW = y.shape
    oC, oH, oW = iC//(pH*pW), iH*pH, iW*pW
    y = y.reshape(B, oC, pH, pW, iH, iW)
    y = y.permute(0, 1, 4, 2, 5, 3)     # B, oC, iH, pH, iW, pW
    y = y.reshape(B, oC, oH, oW)
    return y


def pixelshuffle_invert(x, factor_hw):
    pH = factor_hw[0]
    pW = factor_hw[1]
    y = x
    B, iC, iH, iW = y.shape
    oC, oH, oW = iC*(pH*pW), iH//pH, iW//pW
    y = y.reshape(B, iC, oH, pH, oW, pW)
    y = y.permute(0, 1, 3, 5, 2, 4)     # B, iC, pH, pW, oH, oW
    y = y.reshape(B, oC, oH, oW)
    return y

# def pixelshuffle(x: torch.Tensor, factor_hw: tuple[int, int]):
#     pH = factor_hw[0]
#     pW = factor_hw[1]
#     y = x
#     B, iC, iH, iW = y.shape
#     oC, oH, oW = iC//(pH*pW), iH*pH, iW*pW
#     y = y.reshape(B, oC, pH, pW, iH, iW)
#     y = y.permute(0, 1, 4, 2, 5, 3)     # B, oC, iH, pH, iW, pW
#     y = y.reshape(B, oC, oH, oW)
#     return y


# def pixelshuffle_invert(x: torch.Tensor, factor_hw: tuple[int, int]):
#     pH = factor_hw[0]
#     pW = factor_hw[1]
#     y = x
#     B, iC, iH, iW = y.shape
#     oC, oH, oW = iC*(pH*pW), iH//pH, iW//pW
#     y = y.reshape(B, iC, oH, pH, oW, pW)
#     y = y.permute(0, 1, 3, 5, 2, 4)     # B, iC, pH, pW, oH, oW
#     y = y.reshape(B, oC, oH, oW)
#     return y