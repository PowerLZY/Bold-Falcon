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

"""
sample = load_binaries(train_data_path+"Backdoor.Win32.Agent.bflv_ce22.exe", first_n_byte)
exe_input = torch.from_numpy(sample).unsqueeze(0)

exe_input = exe_input.cuda() if use_gpu else exe_input
exe_input = Variable(exe_input.long(), requires_grad=False)

pred = model(exe_input)

"""

