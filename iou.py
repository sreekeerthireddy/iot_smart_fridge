# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 21:56:13 2021

@author: SreeKeerthiGudipatiR
"""

import torch
import torchvision.ops.boxes as bops

xc=49.78
yc=53.25
w=56.17
h=57.20

x= round(xc-w/2)
y= round(yc-h/2)

xe=x+w
ye=y+h

print(x)
print(y)
print(xe)
print(ye)

b1=torch.tensor([[22, 15, 72, 73]], dtype= torch.float)
b2=torch.tensor([[x,y,xe,ye]], dtype= torch.float)

iou=bops.box_iou(b1, b2)
print("iou value--")
print(iou)
