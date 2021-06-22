import sys
sys.path.append("..")

from modules.detection.instance import Instance
from modules.detection.loader import Loader
from modules.processing.cuckooml import ML
from pprint import pprint

relabelled = True  # False
read_from = "../sample_data/sample"
save_in = "../sample_data/dict"

"""if your data was not produced with one of the latest cuckoo versions there might be a hance that you're missing data labels; in this case you need to run labeling process independently; to do so please follow the guideline below.)
If you have just got the data from the above code cell you need to execute the code below"""
if relabelled:
    import json
    import os
    import sys
    from lib.cuckoo.common.virustotal import VirusTotalAPI

    if not os.path.exists(save_in):
        os.makedirs(save_in)
    vt = VirusTotalAPI("", 0, 0)

    for f in os.listdir(read_from):
        with open(read_from + "/" + f, "r") as malware_report:
            try:
                report = json.load(malware_report)
            except ValueError, error:
                print >> sys.stderr, "Could not load file;", malware_report, "is not a valid JSON file."
                print >> sys.stderr, "Exception: %s" % str(error)
                print >> sys.stderr, "Moving on to the next file..."
                continue

            if report["virustotal"].get("scans") is not None:
                report["virustotal"]["normalized"] = {
                    "cve": "",
                    "platform": "",
                    "metatype": "",
                    "type": "",
                    "family": ""
                }

                norm_lower = {
                    "cve": [],
                    "platform": [],
                    "metatype": [],
                    "type": [],
                    "family": [],
                }

                for vendor in report["virustotal"]["scans"]:
                    report["virustotal"]["scans"][vendor]["normalized"] = \
                        vt.normalize(report["virustotal"]["scans"][vendor]["result"])

                    for label_type in report["virustotal"]["scans"][vendor]["normalized"]:
                        norm_lower[label_type] += \
                            report["virustotal"]["scans"][vendor]["normalized"][label_type]

                labeller = Instance()
                for label_type in norm_lower:
                    labeller.label_sample(norm_lower[label_type])
                    report["virustotal"]["normalized"][label_type] = labeller.label

            with open(save_in + "/" + f, "w") as malware_report_updated: # save_in : '../sample_data/dict'
                json.dump(report, malware_report_updated)

# The first stage is to load the data from the directory holding all the JSONs
loader = Loader()
loader.load_binaries("../sample_data/dict")

# Then we extract all the relevant information from the loaded samples.
simple_features_dict = loader.get_simple_features()
features_dict = loader.get_features()
labels_dict = loader.get_labels()