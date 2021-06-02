# coding=utf-8
import collections
import json
import logging
import os

from cuckoo.common.abstracts import Detection
from cuckoo.common.config import config
from cuckoo.core.database import Database
from cuckoo.core.extract import ExtractManager
from cuckoo.common.exceptions import CuckooProcessingError

log = logging.getLogger(Detection)
class MyDetection():
    """

    """
    def extract_features(self):
    # 数据预处理
        pass

    def fit(self, X, y):
    # 模型训练
        pass

    def predict(self, Y):
    # 预测⽬标值
        predict = []
        return predict

    def run(self):
        """Run extract of printable strings.
        @return: list of printable strings.
        """
        self.key = "strings"
        strings = []

        if self.task["category"] == "file":
            if not os.path.exists(self.file_path):
                raise CuckooProcessingError(
                    "Sample file doesn't exist: \"%s\"" % self.file_path
                )

            try:
                data = open(self.file_path, "rb").read(self.MAX_FILESIZE)
            except (IOError, OSError) as e:
                raise CuckooProcessingError("Error opening file %s" % e)

            strings = []
            for s in re.findall(b"[\x1f-\x7e]{6,}", data):
                strings.append(s.decode("utf-8"))
            for s in re.findall(b"(?:[\x1f-\x7e][\x00]){6,}", data):
                strings.append(s.decode("utf-16le"))

        # Now limit the amount & length of the strings.
        strings = strings[:self.MAX_STRINGCNT]
        for idx, s in enumerate(strings):
            strings[idx] = s[:self.MAX_STRINGLEN]

        return strings