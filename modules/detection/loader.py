# coding=utf-8
# Copyright (C) 2010-2013 Claudio Guarnieri.
# Copyright (C) 2014-2016 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.


import os
import pandas as pd
from instance import Instance


class Loader(object):
    """Loads instances for analysis and give possibility to extract properties of interest."""
    def __init__(self):
        self.binaries = {}
        self.binaries_location = ""
        self.binaries_updated = False


    def load_binaries_dir(self, directory):
        """Load all binaries' reports from given directory."""
        self.binaries_location = directory + "/"
        # 导入整个文件夹的json
        for f in os.listdir(directory):
            self.binaries[f] = Instance()
            self.binaries[f].load_json(directory+"/"+f, f)
            self.binaries[f].label_sample()
            self.binaries[f].extract_features()
            self.binaries[f].extract_basic_features()

    def update_binaries(self, elements, root, locations):
        """在给定的位置将“elements”附加到加载的json"""
        if isinstance(elements, pd.DataFrame) and isinstance(locations, dict):
            self.binaries_updated = True
            for i in elements.index:
                for j in elements.columns:
                    self.binaries[i].update(elements[j][i], root+[locations[j]])
        elif isinstance(locations, str):
            self.binaries_updated = True
            for i in self.binaries:
                self.binaries[i].update(elements, root+[locations])


    def save_binaries(self, alternative_location=""):
        """Save the binaries to given location if they have been updated."""
        if self.binaries_updated:
            save_location = self.binaries_location
            if alternative_location:
                save_location = alternative_location
                if save_location[-1] != "/":
                    save_location += "/"

            # Create directory if it does not exist
            if not os.path.exists(save_location):
                os.makedirs(save_location)

            for f in self.binaries:
                self.binaries[f].save_json(save_location)
            self.binaries_updated = False
        else:
            print "The binaries haven't been updated. No need to save them."


    def get_labels(self):
        """Return binary labels as a labelled dictionary."""
        labels = {}
        for i in self.binaries:
            labels[i] = self.binaries[i].label
        return labels


    def get_features(self):
        """Return complex binary features as a labelled dictionary."""
        features = {}
        for i in self.binaries:
            features[i] = self.binaries[i].features
        return features


    def get_simple_features(self):
        """Return simplified binary features as a labelled dictionary."""
        simple_features = {}
        for i in self.binaries:
            simple_features[i] = self.binaries[i].basic_features
        return simple_features