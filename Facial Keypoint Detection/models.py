import torch
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()        
        self.conv1 = nn.Conv2d(1, 32, 3, padding=0)
        self.batchnorm1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=0)
        self.batchnorm2 = nn.BatchNorm2d(64)
        self.conv3 = nn.Conv2d(64, 128, 3, padding=0) # 7x7
        self.batchnorm3 = nn.BatchNorm2d(128)
        self.conv4 = nn.Conv2d(128, 256, 1, padding=0)
        self.batchnorm4 = nn.BatchNorm2d(256)
        self.conv5 = nn.Conv2d(256, 256, 1, padding=0)
        self.batchnorm5 = nn.BatchNorm2d(256)
        
        self.fc1 = nn.Linear(256*6*6, 2048)
        self.fc2 = nn.Linear(2048, 1024)
        self.fc3 = nn.Linear(1024, 136)
        self.pool = nn.MaxPool2d(2, 2)
        self.pool4x = nn.MaxPool2d(4, 4)
        self.dropout = nn.Dropout(p=0.35)  
        
    def forward(self, x):      
        x = self.pool(F.relu(self.batchnorm1(self.conv1(x))))
        x = self.pool(F.relu(self.batchnorm2(self.conv2(x))))
        x = self.pool(F.relu(self.batchnorm3(self.conv3(x))))
        x = self.pool(F.relu(self.batchnorm4(self.conv4(x))))
        x = self.pool(F.relu(self.batchnorm5(self.conv5(x))))
        
        x = x.view(x.shape[0], -1)
        x = self.dropout(F.relu(self.fc1(x)))
        x = self.dropout(F.relu(self.fc2(x)))
        out = self.fc3(x)        
        return out