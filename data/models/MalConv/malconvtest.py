import os
import sys
import torch
from model import PreMalConv
from lib.cuckoo.common.constants import CUCKOO_ROOT

madel_path = os.path.join(CUCKOO_ROOT, "data", "models", "MalConv","pretrained_malconv.pth")

model = PreMalConv()
model.load_state_dict(torch.load(madel_path, map_location='cpu'))
model.eval()
