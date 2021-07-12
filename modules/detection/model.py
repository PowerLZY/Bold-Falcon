# coding=utf-8
# Copyright (C) 2020-2021 PowerLZY.
# This file is part of Bold-Falcon - https://github.com/PowerLZY/Bold-Falcon
# See the file 'docs/LICENSE' for copying permission.

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset

class MalConv(nn.Module):

	def __init__(self,input_length=2000000,window_size=500):
		super(MalConv, self).__init__()

		self.embed = nn.Embedding(257, 8, padding_idx=0)

		self.conv_1 = nn.Conv1d(4, 128, window_size, stride=window_size, bias=True)
		self.conv_2 = nn.Conv1d(4, 128, window_size, stride=window_size, bias=True)

		self.BatchNorm1d = nn.BatchNorm1d(128)

		self.pooling = nn.MaxPool1d(int(input_length/window_size))

		self.fc_1 = nn.Linear(128,128)
		self.fc_2 = nn.Linear(128,1)

		#self.BatchNorm1d = nn.BatchNorm1d(128)

		self.sigmoid = nn.Sigmoid()

		#self.softmax = nn.Softmax()


	def forward(self,x):
		x = self.embed(x)
		# Channel first
		x = torch.transpose(x,-1,-2)

		cnn_value = self.conv_1(x.narrow(-2, 0, 4))
		cnn_value = self.BatchNorm1d(cnn_value)
		gating_weight = self.sigmoid(self.conv_2(x.narrow(-2, 4, 4)))

		x = cnn_value * gating_weight
		x = self.pooling(x)

		x = x.view(-1,128)
		x = self.fc_1(x)
		x = self.BatchNorm1d(x)
		x = self.fc_2(x)
		#x = self.sigmoid(x)

		return x

class PreMalConv(nn.Module):
	"""
	Architecture implementation.


	def __init__(self, pretrained_path=None, embedding_size=8, max_input_size=2 ** 20):
		super(MalConv, self).__init__(embedding_size, max_input_size, 256, False)
		self.embedding_1 = nn.Embedding(num_embeddings=257, embedding_dim=embedding_size)
		self.conv1d_1 = nn.Conv1d(in_channels=embedding_size, out_channels=128, kernel_size=(500,), stride=(500,),
								  groups=1, bias=True)
		self.conv1d_2 = nn.Conv1d(in_channels=embedding_size, out_channels=128, kernel_size=(500,), stride=(500,),
								  groups=1, bias=True)
		self.dense_1 = nn.Linear(in_features=128, out_features=128, bias=True)
		self.dense_2 = nn.Linear(in_features=128, out_features=1, bias=True)
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

