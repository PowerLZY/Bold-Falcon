# coding=utf-8
import os.path
import numpy as np

from model import *
from lib.cuckoo.common.abstracts import Detection
from lib.cuckoo.common.exceptions import CuckooDetectionError
from lib.cuckoo.common.constants import CUCKOO_ROOT

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset
from torch.autograd import Variable


class MalConv(Detection):
    """
    Providing the raw bytes from a file as input to a convolutional neural network
    which then classifies the given binary as either malicious or benign
    """

    def load_model(self):
        '''
        load model with pretrained_malconv.pth
        :return: model
        '''
        try:
            madel_path = os.path.join(CUCKOO_ROOT, "data", "models", "MalConv", "pretrained_malconv.pth")
            model = PreMalConv()
            model.load_state_dict(torch.load(madel_path, map_location='cpu'))
        except:
            raise CuckooDetectionError("The Detection module malconv has missing load_model!")

        return model

    def run(self):
        """
        Run extract of printable strings with Ngram into XGBoost model.
        :return: predict 结果.
        """
        self.key = "MalConv"
        self.features_type = "static"
        result = None


        #if self.task["category"] == "file":
        """
            features not in json 
            if not os.path.exists(self.file_path):
                raise CuckooDetectionError("Sample file doesn't exist: \"%s\"" % self.file_path)

            try:
                data = open(self.file_path, "r").read()
            except (IOError, OSError) as e:
                raise CuckooDetectionError("Error opening file %s" % e)
        """
        # 导入报告内的特征
        sample = self.binaries.load_binaries(self.file_path)
        exe_input = torch.from_numpy(sample).unsqueeze(0)
        exe_input = Variable(exe_input.long(), requires_grad=False)
        # 导入模型（特征工程+预测模型）
        model = self.load_model()
        model.eval()
        # 模型预测
        result = model(exe_input)

        return np.float(result.detach().cpu().numpy()[0,0])


class PreMalConv(nn.Module):
    """
    Architecture implementation.
    """

    def __init__(self, input_length=2 ** 20, window_size=500):
        super(PreMalConv, self).__init__()

        self.embedding_1 = nn.Embedding(257, 8, padding_idx=0)

        self.conv1d_1 = nn.Conv1d(8, 128, window_size, stride=window_size, bias=True)
        self.conv1d_2 = nn.Conv1d(8, 128, window_size, stride=window_size, bias=True)

        self.pooling = nn.MaxPool1d(int(input_length / window_size))

        self.dense_1 = nn.Linear(128, 128)
        self.dense_2 = nn.Linear(128, 1)

        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.embedding_1(x)
        # Channel first
        x = torch.transpose(x, -1, -2)

        cnn_value = self.conv1d_1(x)
        cnn_value = torch.relu(cnn_value)
        gating_weight = self.sigmoid(self.conv1d_2(x))

        x = cnn_value * gating_weight

        global_max_pooling1d_1 = F.max_pool1d(input=x, kernel_size=x.size()[2:])
        global_max_pooling1d_1_flatten = global_max_pooling1d_1.view(global_max_pooling1d_1.size(0), -1)

        x = torch.relu(self.dense_1(global_max_pooling1d_1_flatten))
        dense_1_activation = torch.relu(x)
        dense_2 = self.dense_2(x)
        dense_2_activation = torch.sigmoid(dense_2)

        return dense_2_activation


class ExeDataset(Dataset):
    '''
    Dataset preparation
    '''
    def __init__(self, fp_list, data_path, label_list = None, first_n_byte=2000000):
        """
            Dataset preparation

            Parameters
            ----------
            fp_list : list
                file name list
            data_path : str
                dataset path
            label_list : list
                label list
            first_n_byte : int, optional, default 2000000
                the max raw bytes
        """
        self.fp_list = fp_list
        self.data_path = data_path
        self.label_list = label_list
        self.first_n_byte = first_n_byte
        # ToDo: 自动载入数据

    def __len__(self):
        """
        返回数据集item数
        """
        return len(self.fp_list)

    def __getitem__(self, idx):
        """
        返回一条训练数据，并将其转换成tensor
        """
        try:
            with open(self.data_path + self.fp_list[idx],'rb') as f:
                tmp = [i+1 for i in f.read()[:self.first_n_byte]] # index 0 will be special padding index 每个值加一
                tmp = tmp+[0]*(self.first_n_byte-len(tmp))
        except:
            with open(self.data_path + self.fp_list[idx].lower(),'rb') as f:
                tmp = [i+1 for i in f.read()[:self.first_n_byte]]
                tmp = tmp+[0]*(self.first_n_byte-len(tmp))
            return np.array(tmp), np.array([self.label_list[idx]])
