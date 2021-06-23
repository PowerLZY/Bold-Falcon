# Copyright (C) 2010-2013 Claudio Guarnieri.
# Copyright (C) 2014-2016 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from modules.detection.instance import Instance

get_data = True

if get_data:
    import os
    import tarfile
    import urllib

    data_root = "../sample_data/"
    if not os.path.exists(data_root):
        os.makedirs(data_root)

    data_filename = "sample.tar.gz"
    urllib.urlretrieve("https://gist.github.com/So-Cool/8ca88add639b41d33b13228f18be6baa/raw/07ac42e555e9b49b13b6a3e71cea7502efd4bd88/sample.tar.gz", data_root+data_filename)

    tar = tarfile.open(data_root+data_filename, "r:gz")
    tar.extractall(path=data_root+data_filename.split('.')[0]+"/")
    tar.close()

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
