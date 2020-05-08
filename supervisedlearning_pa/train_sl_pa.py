from torch.autograd import Variable
from ..util import get_pa_maps
from ..util import sl_df_from_traj
from .LR import LRNet
import torch.nn as nn
import torch.optim as optim

def train_epoch(train_X,train_Y,model,opt,criterion,batch_size=50):
    model.train()
    losses = []

    for beg_i in range(0,train_X.size(0),batch_size):
        x_batch = train_X[beg_i:beg_i + batch_size, :]
        y_batch = train_Y[beg_i:beg_i + batch_size, :]
        x_batch = Variable(x_batch)
        y_batch = Variable(y_batch)

        opt.zero_grad()
        # (1) Forward
        y_hat = model.forward(x_batch)

        # print(y_hat.shape)
        # print(y_batch.shape)
        # (2) Compute diff
        loss = criterion(y_hat, y_batch)
        # (3) Compute gradients
        loss.backward()
        # (4) update weights
        opt.step()
        losses.append(loss.data.numpy())
    return [sum(losses) / float(len(losses))]

def get_training_data():
    p_map,a_map = get_pa_maps()
    trajectories = '../rmn/models/trajectories.log'
    train_df,num_desc = sl_df_from_traj(trajectories,p_map,a_map)
    x_data = train_df['p1','p2','a1','a2'].values()
    print(x_data)
    num_desc = 20
    y_data = train_df[['Topic {}'.format(x) for x in range(num_desc)]]

if __name__ == '__main__':
    net = LRNet()
    opt = optim.Adam(net.parameters())
    criterion = nn.CrossEntropyLoss()