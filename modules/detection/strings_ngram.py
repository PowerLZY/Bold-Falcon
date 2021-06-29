# coding=utf-8
import os.path
import re
from modules.detection.loader import Loader
from lib.cuckoo.common.abstracts import Detection
from lib.cuckoo.common.exceptions import CuckooDetectionError


class Strings_ngram(Detection):
    """描述"""

    # 特征提取
    # 特征工程
    # 特征保存pandas
    def load_binaries(self, json_path):
        pass

    def load_features(self, features_dict):
        pass


    def load_model(self):
        pass


    def predict(self):
        pass


    def run(self):
        """
        Run extract of printable strings.
        @return: list of printable strings.
        """
        self.key = "Strings_ngram"
        self.features_type = "static"
        result = None

        if self.task["category"] == "file":
            if not os.path.exists(self.file_path):
                raise CuckooDetectionError("Sample file doesn't exist: \"%s\"" % self.file_path)

            try:
                data = open(self.file_path, "r").read()
            except (IOError, OSError) as e:
                raise CuckooDetectionError("Error opening file %s" % e)

            # The first stage is to load the data from the directory holding all the JSONs
            loader = Loader()
            loader.load_binaries(self.json_path)

            # Then we extract all the relevant information from the loaded samples.
            features_dict = loader.get_features()

            self.load_features(features_dict)

            # 特征工程
            self.features  # panads

            # 导入模型
            self.load_model()

            # 预测结果
            result = self.predict(self.features)

        return result

