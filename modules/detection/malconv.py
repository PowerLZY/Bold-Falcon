# coding=utf-8
import os.path

from model import *
from lib.cuckoo.common.abstracts import Detection
from lib.cuckoo.common.exceptions import CuckooDetectionError
from lib.cuckoo.common.constants import CUCKOO_ROOT

from torch.autograd import Variable


class MalConv(Detection):
    """描述"""

    def load_model(self):

        try:
            madel_path = os.path.join(CUCKOO_ROOT, "data", "models", "MalConv", "pretrained_malconv.pth")
            model = PreMalConv()
            model.load_state_dict(torch.load(madel_path, map_location='cpu'))
            model.eval()
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
        use_cpu = 1
        use_gpu = True
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

        exe_input = exe_input.cuda() if use_gpu else exe_input
        exe_input = Variable(exe_input.long(), requires_grad=False)
        # 导入模型（特征工程+预测模型）
        model = self.load_model()
        # 模型预测
        result = model(exe_input)

        return result.detach().cpu().numpy()[0,0]

