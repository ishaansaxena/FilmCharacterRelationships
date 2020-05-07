import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

class LRNet(nn.Module):
    def _init_(self,number_classes):
        super(LRNet,self).__init__()
        self.act = nn.Softmax()

    def forward(self,input):
        y = self.act()