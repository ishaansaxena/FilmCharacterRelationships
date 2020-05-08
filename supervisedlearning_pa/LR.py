import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

class LRNet(nn.Module):
    def _init_(self,feature_dimension,number_classes):
        super(LRNet,self).__init__()
        self.fc1 = nn.Linear(feature_dimension,number_classes)
        self.act = nn.Softmax()

    def forward(self,input):
        dot_fc1 = self.fc1(input)
        y = self.act1(dot_fc1)


