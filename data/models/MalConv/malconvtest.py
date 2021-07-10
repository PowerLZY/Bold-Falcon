# coding=utf-8
import os
import sys
import torch
from model import *
from torch.utils.data import DataLoader
from torch.autograd import Variable

from lib.cuckoo.common.constants import CUCKOO_ROOT

madel_path = os.path.join(CUCKOO_ROOT, "data", "models", "MalConv","pretrained_malconv.pth")
"""
model = PreMalConv()
model.load_state_dict(torch.load(madel_path, map_location='cpu'))
model.eval()
"""

use_cpu  = 1
use_gpu = None
train_data_path = " " # 样本路径
filename = " " # 样本名称
labels = " " # 样本标签
first_n_byte = 2000000# 字节前n
batch_size = 1# 抽样数量


malconv = PreMalConv()
malconv.load_state_dict(torch.load(madel_path, map_location='cpu'))
malconv.eval()




# 文件名列表、数据文件夹、文件列表标签、前n位字节
validloader = DataLoader(ExeDataset(filename, train_data_path, labels, first_n_byte),
                        batch_size=batch_size, shuffle=False, num_workers=use_cpu)

for _, val_batch_data in enumerate(validloader):
    cur_batch_size = val_batch_data[0].size(0)

    exe_input = val_batch_data[0].cuda() if use_gpu else val_batch_data[0]
    exe_input = Variable(exe_input.long(), requires_grad=False)


    pred = malconv(exe_input)
