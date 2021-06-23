# coding=utf-8
import collections
import itertools
import os
import re
from math import log
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from hdbscan import HDBSCAN
from sklearn import metrics
from sklearn.cluster import DBSCAN
from sklearn.manifold import TSNE

from instance import Instance
from loader import Loader

class ML(object):
    """Feature formatting and machine learning for Cuckoo analysed binaries.
    All functions marked with asterisk (*) were inspired by code distributed
    with "Back to the Future: Malware Detection with Temporally Consistent
    Labels" by Brad Miller at al."""
    SIMPLE_CATEGORIES = {
        "properties": [
            "has_authenticode",
            "has_pdb",
            "pe_features",
            "packer_upx",
            "has_wmi"
        ],
        "behaviour": [
            "dumped_buffer2",
            "suspicious_process",
            "persistence_autorun",
            "raises_exception",
            "sniffer_winpcap",
            "injection_runpe",
            "dumped_buffer",
            "exec_crash",
            "creates_service",
            "allocates_rwx"
        ],
        "exploration": [
            "recon_fingerprint",
            "antidbg_windows",
            "locates_sniffer"
        ],
        "mutex": [
            "ardamax_mutexes",
            "rat_xtreme_mutexes",
            "bladabindi_mutexes"
        ],
        "networking": [
            "network_bind",
            "networkdyndns_checkip",
            "network_http",
            "network_icmp",
            "recon_checkip",
            "dns_freehosting_domain",
            "dns_tld_pw",
            "dns_tld_ru"
        ],
        "filesystem": [
            "modifies_files",
            "packer_polymorphic",
            "creates_exe",
            "creates_doc"
        ],
        "security": [
            "rat_xtreme",
            "disables_security",
            "trojan_redosru",
            "worm_renocide",
            "antivirus_virustotal"
        ],
        "virtualisation": [
            "antivm_vbox_files",
            "antivm_generic_bios",
            "antivm_vmware_keys",
            "antivm_generic_services",
            "antivm_vmware_files",
            "antivm_sandboxie",
            "antivm_vbox_keys",
            "antivm_generic_scsi",
            "antivm_vmware_in_instruction",
            "antivm_generic_disk",
            "antivm_virtualpc"
        ],
        "sanbox": [
            "antisandbox_unhook",
            "antisandbox_mouse_hook",
            "antisandbox_foregroundwindows",
            "antisandbox_productid",
            "antisandbox_idletime",
            "antisandbox_sleep"
        ],
        "infostealer": [
            "infostealer_browser",
            "infostealer_mail",
            "infostealer_keylogger",
            "infostealer_ftp",
        ],
        "ransomware": [
            "ransomware_files",
            "ransomware_bcdedit"
        ]
    }

    CATEGORIES = {
        "static": {
            ":meta:": [
                "",
                "size",
                "timestamp"
            ],
            ":sign:": [
                "",
                "signed"
            ],
            ":heur:": [
                ""
            ],
            ":pack:": [
                ""
            ],
            ":pef:": [
                "lang:"
            ],
            ":simp:": [
                "",
                "count"
            ]
        },
        "dynamic": {
            ":dimp:": [
                "",
                "proc:",
                "mutex:"
            ],
            ":file:": {
                "touch:": [
                    ""
                ],
                "count:": [
                    "",
                    "all",
                    "read",
                    "written",
                    "deleted",
                    "copied",
                    "renamed",
                    "opened",
                    "exists",
                    "failed"
                ]
            },
            ":net:": [
                ""
            ],
            ":reg:": [
                "",
                "write:",
                "del:"
            ],
            ":win:": [
                ""
            ]
        },
        "counts": {
            ":count:": {
                "lang": [""],
                "simp": [
                    "",
                    ":"
                ],
                "proc": [""],
                "dimp": [""],
                "file:": [
                    "",
                    "all",
                    "read",
                    "written",
                    "deleted",
                    "copied",
                    "renamed",
                    "opened",
                    "exists",
                    "failed"
                ],
                "tcp": [""],
                "udp": [""],
                "dns": [""],
                "http": [""],
                "reg:": [
                    "",
                    "write",
                    "del"
                ],
                "wapi": [""]
            }
        }
    }

    PATTERNS = [r"Armadillo", r"PECompact", r"ASPack", r"ASProtect",
                r"Upack", r"U(PX|px)", r"FSG", r"BobSoft Mini Delphi",
                r"InstallShield 2000", r"InstallShield Custom",
                r"Xtreme\-Protector", r"Crypto\-Lock", r"MoleBox", r"Dev\-C\+\+",
                r"StarForce", r"Wise Installer Stub", r"SVK Protector",
                r"eXPressor", r"EXECryptor", r"N(s|S)Pac(k|K)", r"KByS",
                r"themida", r"Packman", r"EXE Shield", r"WinRAR 32-bit SFX",
                r"WinZip 32-bit SFX", r"Install Stub 32-bit", r"P(E|e)tite",
                r"PKLITE32", r"y(o|0)da's (Protector|Crypter)", r"Ste@lth PE",
                r"PE\-Armor", r"KGB SFX", r"tElock", r"PEBundle", r"Crunch\/PE",
                r"Obsidium", r"nPack", r"PEX", r"PE Diminisher",
                r"North Star PE Shrinker", r"PC Guard for Win32", r"W32\.Jeefo",
                r"MEW [0-9]+", r"InstallAnywhere", r"Anskya Binder",
                r"BeRoEXEPacker", r"NeoLite", r"SVK\-Protector",
                r"Ding Boy's PE\-lock Phantasm", r"hying's PEArmor", r"E language",
                r"NSIS Installer", r"Video\-Lan\-Client", r"EncryptPE",
                r"HASP HL Protection", r"PESpin", r"CExe", r"UG2002 Cruncher",
                r"ACProtect", r"Thinstall", r"DBPE", r"XCR", r"PC Shrinker",
                r"AH(p|P)ack", r"ExeShield Protector",
                r"\* \[MSLRH\]", r"XJ \/ XPAL", r"Krypton", r"Stealth PE",
                r"Goats Mutilator", r"PE\-PACK", r"RCryptor", r"\* PseudoSigner",
                r"Shrinker", r"PC-Guard", r"PELOCKnt", r"WinZip \(32\-bit\)",
                r"EZIP", r"PeX", r"PE( |\-)Crypt", r"E(XE|xe)()?Stealth",
                r"ShellModify", r"Macromedia Windows Flash Projector\/Player",
                r"WARNING ->", r"PE Protector", r"Software Compress",
                r"PE( )?Ninja", r"Feokt", r"RLPack",
                r"Nullsoft( PIMP)? Install System", r"SDProtector Pro Edition",
                r"VProtector", r"WWPack32", r"CreateInstall Stub", r"ORiEN",
                r"dePACK", r"ENIGMA Protector", r"MicroJoiner", r"Virogen Crypt",
                r"SecureEXE", r"PCShrink", r"WinZip Self\-Extractor",
                r"PEiD\-Bundle", r"DxPack", r"Freshbind", r"kkrunchy"]

    def __init__(self, context="standalone"):
        """The context variable defines type of operation for the functions
        using visualisations. *standalone* saves figures as files, *notebook*
        displays them."""
        self.context = context  # 'notebook' 预留接口在jupyter显示
        self.labels = None
        self.simple_features = None
        self.simple_features_description = {}
        self.features = None
        self.clustering = {}

    def __log_bin(self, value, base=3):
        """Return a logarithmic bin of given value. * """
        if value is None:
            return None

        # Add base -1 to count so that 0 is in its own bin
        return int(log(value + base - 1, base))

    def __normalise_string(self, string):
        """Get lower case string representation. * """
        if string is None:
            return None

        return string.lower()

    def __simplify_string(self, string, distinguish_voyels=False):
        """Returns a simplified representation of the string where characters
        are mapped to their representatives. * """
        if string is None:
            return None

        nums = re.compile(r"[0-9]")
        caps = re.compile(r"[A-Z]")
        smal = re.compile(r"[a-z]")
        caps_c = re.compile(r"[QWRTPSDFGHJKLZXCVBNM]")
        caps_v = re.compile(r"[EYUIOA]")
        smal_c = re.compile(r"[qwrtpsdfghjklzxcvbnm]")
        smal_v = re.compile(r"[eyuioa]")

        string = nums.sub('0', string)

        if distinguish_voyels:
            string = caps_c.sub('B', string)
            string = caps_v.sub('A', string)
            string = smal_c.sub('b', string)
            string = smal_v.sub('a', string)
            return string

        string = caps.sub('A', string)
        string = smal.sub('a', string)
        return string

    def __n_grams(self, string, n=3, reorder=False):
        """Returns a *set* of n-grams. If the iterable is smaller than n, it is
        returned itself. * """
        if string is None:
            return None

        if len(string) <= n:
            if reorder:
                return set(["".join(sorted(string))])
            return set([string])

        ngrams = set()
        for i in range(0, len(string) - n + 1):
            if reorder:
                ngrams.add("".join(sorted(string[i:i + n])))
            else:
                ngrams.add(string[i:i + n])

        return ngrams

    def __handle_string(self, string):
        """Apply normalisation, simplification and n-gram extraction to a
        string. If the string is missing (None) return empty list."""
        handled = self.__n_grams(
            self.__simplify_string(
                self.__normalise_string(string)
            )
        )
        if handled is None:
            return []
        else:
            return handled

    def extract_labels(self, labels):
        """Extract labels into pandas data frame."""
        return pd.DataFrame(labels, index=["label"]).T

    def load_labels(self, labels):
        """Load labels into pandas data frame."""
        self.labels = self.extract_labels(labels)

    # 提取简单特征
    def extract_simple_features(self, simple_features):
        """Extract simple features form an external object into pandas data
        frame."""
        simple_features = pd.DataFrame(simple_features).T  # transpose
        simple_features.fillna(False, inplace=True)
        # Convert to bool: True/False
        simple_features = simple_features.astype(bool)
        # Change to int: 1/0
        simple_features = simple_features.astype(int)

        # Aggregate features descriptions
        simple_features_description = {}
        for binary in simple_features:
            for token in simple_features[binary]:
                if token not in simple_features_description:
                    simple_features_description[token] = \
                        simple_features[binary][token]

        return simple_features, simple_features_description

    def load_simple_features(self, simple_features):
        """Load simple features form an external object into pandas data
        frame."""
        self.simple_features, self.simple_features_description = \
            self.extract_simple_features(simple_features)

    def export_simple_dataset(self, filename="simple_dataset.csv"):
        """Export a dataset consisting of malware labels and *simple* features to CSV formatted file."""
        # Check if data and labels are loaded
        if self.simple_features is None:
            print "Please load simple features first."
            return

        if self.labels is None:
            print "Please load labels first."
            return

        simple_dataset = pd.concat([self.simple_features, self.labels], axis=1)
        simple_dataset.to_csv(filename)

    def simple_feature_category(self, category="properties"):
        """Get simple feature data frame containing only features form selected category."""
        if self.simple_features is None:
            print "Simple features are not loaded. Please load them before \
                   extracting categories."
            return None

        return self.simple_features.loc[:, self.SIMPLE_CATEGORIES[category]]

    # 提取完整特征
    def extract_features(self, features, include_API_calls=False, include_API_calls_count=False):
        """Extract features form an external object into pandas data frame."""
        my_features = {}
        for i in features:
            my_features[i] = {}

            # Exponentially bin the binary size and timestamp
            my_features[i][":meta:size"] = self.__log_bin(features[i]["size"])
            my_features[i][":meta:timestamp"] = \
                self.__log_bin(features[i]["timestamp"])

            # Handle ExifTool output
            exif = ["FileDescription", "OriginalFilename", "magic_byte"]
            for e in exif:
                for j in self.__handle_string(features[i][e]):
                    my_features[i][":meta:" + j] = 1

            # Is the binary signed?
            my_features[i][":sign:signed"] = int(features[i]["signed"])
            # And other signature features
            signature = ["Comments", "ProductName", "LegalCopyright",
                         "InternalName", "CompanyName"]
            for s in signature:
                for j in self.__handle_string(features[i][s]):
                    my_features[i][":sign:" + j] = 1

            # Extract packer
            regexps = [re.compile(pattern) for pattern in self.PATTERNS]
            if features[i]["packer"] is not None:
                for packer in features[i]["packer"]:
                    for regexp in regexps:
                        if regexp.search(packer):
                            my_features[i][":pack:" + regexp.pattern] = 1
                            break

            # Vectorise PEFs
            for j in features[i]["languages"]:
                j_norm = self.__normalise_string(j)
                my_features[i][":pef:lang:" + j_norm] = 1
            # Get number of languages
            my_features[i][":count:lang"] = len(features[i]["languages"])
            # TODO: handle *section_attrs* and *resource_attrs*

            # Categorise static imports
            # TODO: use binning for this count
            my_features[i][":simp:count"] = \
                features[i]["static_imports"]["count"]
            static_imports_dlls = features[i]["static_imports"].keys()
            static_imports_dlls.remove("count")
            # Count static imports
            my_features[i][":count:simp"] = len(static_imports_dlls)
            for j in static_imports_dlls:
                my_features[i][":simp:" + j] = 1
                # TODO: include API calls?
                if include_API_calls:
                    for k in features[i]["static_imports"][j]:
                        my_features[i][":simp:" + j + ":" + k] = 1
                # Count static imports API calls
                if include_API_calls_count:
                    my_features[i][":count:simp:" + j] = \
                        len(features[i]["static_imports"][j])

            # Categorise dynamic imports
            if features[i]["mutex"] is not None:
                for mutex in features[i]["mutex"]:
                    for j in self.__handle_string(mutex):
                        my_features[i][":dimp:mutex:" + j] = 1
                # Count mutexes
                my_features[i][":count:mutex"] = len(features[i]["mutex"])
            for process in features[i]["processes"]:
                my_features[i][":dimp:proc:" + process] = 1
            # Count processes
            my_features[i][":count:proc"] = len(features[i]["processes"])
            for di in features[i]["dynamic_imports"]:
                my_features[i][":dimp:" + di] = 1
            # Count dynamic imports
            my_features[i][":count:dimp"] = \
                len(features[i]["dynamic_imports"])

            # File operations
            # TODO: tell apart different file operations by prefixing
            # Files touched
            touch = ["file_read", "file_written", "file_deleted", "file_copied",
                     "file_renamed"]
            for t in touch:
                for f in features[i][t]:
                    my_features[i][":file:touch:" + f] = 1
            # TODO: better binning (linear not logarithmic)
            # File numbers
            operation_number = [("all", "files_operations"),
                                ("read", "files_read"),
                                ("written", "files_written"),
                                ("deleted", "files_deleted"),
                                ("copied", "files_copied"),
                                ("renamed", "files_renamed"),
                                ("opened", "files_opened"),
                                ("exists", "files_exists"),
                                ("failed", "files_failed")]
            for o in operation_number:
                my_features[i][":file:count:" + o[0]] = \
                    self.__log_bin(features[i][o[1]])
                my_features[i][":count:file:" + o[0]] = \
                    features[i][o[1]]

            # Networking
            # TODO: include subnets
            # TODO: tell apart type of connection: prefix features with "tcp",
            #       "udp", "dns"
            for tcp in features[i]["tcp"]:
                my_features[i][":net:" + tcp] = 1
            for udp in features[i]["udp"]:
                my_features[i][":net:" + udp] = 1
            for dns in features[i]["dns"]:
                my_features[i][":net:" + dns] = 1
                for j in features[i]["dns"][dns]:
                    my_features[i][":net:" + j] = 1
            for http in features[i]["http"]:
                my_features[i][":net:" + features[i]["http"][http]["host"]] \
                    = 1
            # Count tcp addresses
            my_features[i][":count:tcp"] = len(features[i]["tcp"])
            # Count udp addresses
            my_features[i][":count:udp"] = len(features[i]["udp"])
            # Count dns addresses
            my_features[i][":count:dns"] = len(features[i]["dns"])
            # Count http addresses
            my_features[i][":count:http"] = len(features[i]["http"])

            # Register operations
            for rw in features[i]["regkey_written"]:
                my_features[i][":reg:write:" + rw] = 1
            # Count register keys written
            my_features[i][":count:reg:write"] = \
                len(features[i]["regkey_written"])
            for rd in features[i]["regkey_deleted"]:
                my_features[i][":reg:del:" + rd] = 1
            # Count register keys written
            my_features[i][":count:reg:del"] = \
                len(features[i]["regkey_deleted"])

            # Windows API
            # TODO: better binning (linear not logarithmic)
            for wapi in features[i]["api_stats"]:
                my_features[i][":win:" + wapi] = \
                    self.__log_bin(features[i]["api_stats"][wapi])
            # Count Windows API calls
            my_features[i][":count:wapi"] = len(features[i]["api_stats"])

        # Make Pandas DataFrame from the dictionary
        features_pd = pd.DataFrame(my_features).T
        # TODO: the operation below cannot tell apart missing vales and None
        features_pd.fillna(0, inplace=True)
        return features_pd

    def load_features(self, features, include_API_calls=False, include_API_calls_count=False):
        """Load features form an external object into pandas data frame."""

        self.features = self.extract_features(features, include_API_calls, include_API_calls_count)

    def export_dataset(self, filename="dataset.csv"):
        """Export a dataset consisting of malware labels and features to CSV formatted file."""
        # Check if data and labels are loaded
        if self.features is None:
            print "Please load features first."
            return

        if self.labels is None:
            print "Please load labels first."
            return

        dataset = pd.concat([self.features, self.labels], axis=1)
        dataset.to_csv(filename, encoding='utf-8')

    def feature_category(self, category="static", complement=False):
        """Get feature data frame containing only features form selected category (or their complement)."""

        def pull_names(obj, prefix=""):
            ret = []
            if isinstance(obj, dict):
                if prefix: ret.append(prefix)
                for key in obj:
                    ret += pull_names(obj[key], prefix + key)
                return ret
            elif isinstance(obj, list):
                for i in obj:
                    ret.append(prefix + i)
                return ret

        if self.features is None:
            print "Features are not loaded. Please load them before extracting \
                   categories."
            return None

        # Pull all possible categories
        categories = self.CATEGORIES.keys()
        for cat in self.CATEGORIES:
            categories += pull_names(self.CATEGORIES[cat])

        # Check if chosen category is available
        if category not in categories:
            print "Chosen category:", category, "is not available.\n\
                   please choose one of the following:"
            print ", ".join(categories)
            return None

        # Get a list of specified prefixes
        if category == "static" or category == "dynamic" or category == "count":
            category = pull_names(category)
        else:
            category = [category]

        extract = []
        # TODO: what if we want exact match but most starts with word
        for col in self.features:
            for c in category:
                if complement and not col.startswith(c):
                    extract.append(col)
                elif not complement and col.startswith(c):
                    extract.append(col)

        return self.features.loc[:, extract]

    def filter_dataset(self, dataset=None, feature_coverage=0.1,
                       complement=False):
        """Prune features that are useless."""
        if dataset is None:
            dataset = self.features.copy()

        # Remove sparse features
        row_count = dataset.shape[0]
        remove_features = []
        for col in dataset:
            zero_count = 0.0
            for row in dataset[col]:
                if not row:
                    zero_count += 1
            # XOR
            if complement != (row_count - zero_count) / row_count < feature_coverage:
                remove_features.append(col)
        dataset.drop(remove_features, axis=1, inplace=True)

        return dataset

    def detect_abnormal_behaviour(self, count_dataset=None, figures=True):
        """Detect samples that behave significantly different than others."""
        if count_dataset is None:
            # Pull all count features
            count_features = self.feature_category(":count:")
            meta_size = self.feature_category(":meta:size")
            simp_count = self.feature_category(":simp:count")
            count_dataset = pd.concat([count_features, meta_size, simp_count], axis=1)

        if not figures:
            ret = {}
        for f in count_dataset:
            # Produce boxplots
            if figures:
                sns.boxplot(count_dataset[f])
                sns.swarmplot(count_dataset[f], color=".25")
                plt.title("Abnormal behaviour detection for " + f)
                if self.context == "notebook":
                    plt.show()
                else:
                    plt.savefig("abnormal_behaviour_" + f.replace(":", "_") + \
                                ".png")
                    plt.close()

            # Get list of local outliers
            f_1_quartile = count_dataset[f].quantile(0.25)
            f_3_quartile = count_dataset[f].quantile(0.75)
            f_IQR = f_3_quartile - f_1_quartile
            f_outliers = []
            f_suspected_outliers = []
            for s in count_dataset[f].index:
                if count_dataset[f][s] > f_3_quartile + 3 * f_IQR or \
                        count_dataset[f][s] < f_1_quartile - 3 * f_IQR:
                    f_outliers.append(s)
                    continue
                if count_dataset[f][s] > f_3_quartile + 1.5 * f_IQR or \
                        count_dataset[f][s] < f_1_quartile - 1.5 * f_IQR:
                    f_suspected_outliers.append(s)
            if figures:
                print f
                print "Outliers: ", ", ".join(f_outliers)
                print "Suspected outliers: ", ", ".join(f_suspected_outliers)
                print "------------------------------------------------------------"
            else:
                ret[f] = {"outliers": f_outliers,
                          "suspect_outliers": f_suspected_outliers}
        if not figures:
            return pd.DataFrame(ret).T

    def visualise_data(self, data=None, labels=None, learning_rate=200,
                       fig_name="custom"):
        """Create t-Distributed Stochastic Neighbor Embedding for features and
        labels to help inspect the data."""
        if data is None:
            data = self.features
        if labels is None:
            labels = self.labels

        tsne = TSNE(learning_rate=learning_rate)
        tsne_fit = tsne.fit_transform(data)
        tsne_df = pd.DataFrame(tsne_fit, index=data.index, columns=['0', '1'])
        tsne_dfl = pd.concat([tsne_df, labels], axis=1)

        sns.lmplot("0", "1", data=tsne_dfl, fit_reg=False, hue="label",
                   scatter_kws={"marker": "D", "s": 50}, legend_out=True)
        plt.title(fig_name + " (lr:" + str(learning_rate) + ")")
        if self.context == "notebook":
            plt.show()
        else:
            plt.savefig(fig_name + "_" + str(learning_rate) + ".png",
                        bbox_inches='tight', pad_inches=1.)
            plt.close()

    def save_dataset(self, filename="custom_dataset.csv", features=None, \
                     labels=None):
        """Export a dataset to CSV formatted file."""
        # Check if data and labels are loaded
        if features is None:
            print "You must indicate data to be saved."
            return

        if labels is None:
            print "You didn't indicate labels to be used. Internal labels will \
                   be used."
            if self.labels is None:
                print "Internal labels not available."
                return
            else:
                labels = self.labels

        dataset = pd.concat([features, labels], axis=1)
        dataset.to_csv(filename, encoding='utf-8')
    # 聚类和异常检测
    def cluster_dbscan(self, features=None, eps=20.0, min_samples=5, dry=False):
        """Do *dbscan* clustering and return """
        if features is None:
            print "You didn't indicate features to be used. Internal features \
                will be used."
            if self.features is None:
                print "Internal features not available."
                return
            else:
                features = self.features

        dbscan = DBSCAN(eps=eps, min_samples=min_samples).fit(features)

        # TODO: Allow storing multiple clustering results based on parameters
        if dry:
            return {
                "eps": eps,
                "min_samples": min_samples,
                "clustering": pd.DataFrame(dbscan.labels_, index=features.index,
                                           columns=["label"])
            }
        else:
            # if "dbscan" not in self.clustering:
            # self.clustering["dbscan"] = {}
            # clustering_hash = "eps:%f&min_samples:%d" % (eps, min_samples)
            self.clustering["dbscan"] = {
                # self.clustering["dbscan"][clustering_hash] = {
                "eps": eps,
                "min_samples": min_samples,
                "clustering": pd.DataFrame(dbscan.labels_, index=features.index,
                                           columns=["label"])
            }

    def cluster_hdbscan(self, features=None, min_samples=1, \
                        min_cluster_size=6, dry=False):
        """Do *hdbscan* clustering and return """
        if features is None:
            print "You didn't indicate features to be used. Internal features \
                will be used."
            if self.features is None:
                print "Internal features not available."
                return
            else:
                features = self.features

        hdbscan = HDBSCAN(min_samples=min_samples, \
                          min_cluster_size=min_cluster_size)
        hdbscan_fit = hdbscan.fit(features)
        hdbscan_stats = np.column_stack([hdbscan_fit.labels_,
                                         hdbscan_fit.probabilities_,
                                         hdbscan_fit.outlier_scores_])

        # TODO: Allow storing multiple clustering results based on parameters
        if dry:
            return {
                "min_samples": min_samples,
                "min_cluster_size": min_cluster_size,
                "clustering": pd.DataFrame(hdbscan_stats, index=features.index,
                                           columns=["label", "probability",
                                                    "outlier_score"])
            }
        else:
            # if "hdbscan" not in self.clustering:
            # self.clustering["hdbscan"] = {}
            # clustering_hash = "min_samples:%s&min_cluster_size:%d" % \
            # (min_samples, min_cluster_size)
            # self.clustering["hdbscan"][clustering_hash] = {
            self.clustering["hdbscan"] = {
                "min_samples": min_samples,
                "min_cluster_size": min_cluster_size,
                "clustering": pd.DataFrame(hdbscan_stats, index=features.index,
                                           columns=["label", "probability",
                                                    "outlier_score"])
            }

    def save_clustering_results(self, loader, save_location=""):
        """Update JSONs report files with clustering results"""
        # TODO: Allow storing multiple clustering results based on parameters
        hdbscan_root = ["info", "clustering", "hdbscan"]
        hdbscan_paths = {"label": "clusterID",
                         "probability": "clusterProbability",
                         "outlier_score": "outlierScore"}
        if "hdbscan" in self.clustering:
            loader.update_binaries(self.clustering["hdbscan"]["clustering"],
                                   hdbscan_root, hdbscan_paths)
            loader.update_binaries(self.clustering["hdbscan"]["min_samples"],
                                   hdbscan_root, "min_samples")
            loader.update_binaries(
                self.clustering["hdbscan"]["min_cluster_size"], hdbscan_root,
                "min_cluster_size")

        dbscan_root = ["info", "clustering", "dbscan"]
        dbscan_paths = {"label": "clusterID"}
        if "dbscan" in self.clustering:
            loader.update_binaries(self.clustering["dbscan"]["clustering"],
                                   dbscan_root, dbscan_paths)
            loader.update_binaries(self.clustering["dbscan"]["eps"],
                                   dbscan_root, "eps")
            loader.update_binaries(self.clustering["dbscan"]["min_samples"],
                                   dbscan_root, "min_samples")

        loader.save_binaries(save_location)

    def anomaly_detection(self, samples=None, labels=None,
                          probability_threshold=0.9, outlier_threshold=0.5,
                          homogeneity_threshold=0.2):
        """Detect anomalies in clustering using samples classified as noise and
        low probability cluster membership."""
        if "hdbscan" not in self.clustering:
            print "Soft clustering is needed for *anomaly detection*.", \
                "Currently only *HDBSCAN* is supported."
            return

        if labels is None:
            labels = self.labels
        if samples is None:
            samples = self.clustering["hdbscan"]["clustering"]
        sample = samples.copy()
        sample.rename(columns={"label": "cluster"}, inplace=True)
        sample = pd.concat([sample, labels], axis=1)

        anomalies = {}

        anomalies["outliers"] = sample[sample.cluster == -1].index.tolist()
        # TODO: cluster ID and samples most similar to given outlier

        # Clustered as X but below threshold
        anomalies["low_probability"] = \
            sample.loc[sample.probability < probability_threshold] \
                .loc[sample.cluster != -1].index.tolist()

        # High outlier score
        anomalies["high_outlier_score"] = \
            sample.loc[sample.outlier_score > outlier_threshold] \
                .loc[sample.cluster != -1].index.tolist()

        # Within cluster inconsistencies - detect non-homogeneous clusters
        anomalies["homogeneity_suspects"] = {}
        for i in set(sample["cluster"].tolist()):
            c = collections.Counter(
                sample[sample.cluster == i]["label"].tolist())
            total = float(sum(c.values()))
            suspicious = [j for j in c if c[j] / total < homogeneity_threshold]

            anomalies["homogeneity_suspects"][i] = []
            for j in suspicious:
                anomalies["homogeneity_suspects"][i] += \
                    sample.loc[sample.cluster == i].loc[sample.label == j] \
                        .index.tolist()

        return anomalies

    def compare_sample(self, sample, amend=False):
        """Compare new sample with current clustering."""
        if isinstance(sample, Instance):
            # Retrieve cluster ID
            # TODO: this alters cluster structure-retraining needs to be removed
            features = self.extract_features({"?" + sample.name: sample.features})
            # simple_features = self.extract_simple_features(
            # {"?"+sample.name: sample.basic_features})
            # label = self.extract_labels({"?"+sample.name: sample.label})
            extended_features = pd.concat([self.features, features])
            extended_features.fillna(0, inplace=True)
            clustering = self.cluster_hdbscan(features=extended_features, \
                                              dry=True)
            clustering_result = clustering["clustering"].loc["?" + sample.name]

            # TODO: return samples that are the most similar to the analysed one

            # Save clustering information to the sample's JSON
            if amend:
                root = ["info", "clustering", "hdbscan"]
                sample.update(clustering_result["label"], root + ["clusterID"])
                sample.update(clustering_result["probability"],
                              root + ["clusterProbability"])
                sample.update(clustering_result["outlier_score"],
                              root + ["outlierScore"])
                sample.update(clustering["min_samples"], "min_samples")
                sample.update(clustering["min_cluster_size"], \
                              "min_cluster_size")
                sample.save_json(os.path.dirname(sample.json_path) + "/")
        # TODO: handle more than one test sample
        elif isinstance(sample, Loader):
            clustering_result = pd.DataFrame()

        return clustering_result

    def assess_clustering(self, clustering, labels, data=None,
                          discard_noise=False):
        """Assess clusters fit according to variety of metrics."""

        def performance_metric(clustering, labels, data, noise):
            performance_metrics = {}
            performance_metrics["Adjusted Random Index"] = \
                metrics.adjusted_rand_score(labels, clustering)
            performance_metrics["Adjusted Mutual Information Score"] = \
                metrics.adjusted_mutual_info_score(labels, clustering)
            performance_metrics["Homogeneity"] = \
                metrics.homogeneity_score(labels, clustering)
            performance_metrics["Completeness"] = \
                metrics.completeness_score(labels, clustering)
            performance_metrics["V-measure"] = \
                metrics.v_measure_score(labels, clustering)

            if data is None or noise:
                return performance_metrics
            performance_metrics["Silhouette Coefficient"] = \
                metrics.silhouette_score(data, np.array(clustering))

            return performance_metrics

        cluster_label = clustering["label"].tolist()
        ground_label = labels["label"].tolist()

        if discard_noise:
            clustering = []
            labels = []
            noise_clustering = []
            noise_labels = []
            for c, g in itertools.izip(cluster_label, ground_label):
                if c == -1:
                    noise_clustering.append(c)
                    noise_labels.append(g)
                else:
                    clustering.append(c)
                    labels.append(g)
            # print performance_metric(noise_clustering, noise_labels, \
            #                          data, True)
        else:
            clustering = cluster_label
            labels = ground_label

        return performance_metric(clustering, labels, data, discard_noise)

    def clustering_label_distribution(self, clustering, labels, plot=False):
        """Get statistics about number of ground truth labels per cluster."""
        cluster_ids = set(clustering["label"].tolist())
        labels_ids = set(labels["label"].tolist())
        cluster_distribution = {}
        for i in cluster_ids:
            cluster_distribution[i] = {}
            for j in labels_ids:
                cluster_distribution[i][j] = 0

        for i in clustering.index:
            cluster_distribution[clustering["label"][i]][labels["label"][i]] \
                += 1

        if plot:
            for i in cluster_distribution:
                fig = plt.figure()
                ax = fig.add_subplot(111)
                yticks = []
                counter = 0
                for j in cluster_distribution[i]:
                    if cluster_distribution[i][j]:
                        ax.barh(counter, cluster_distribution[i][j])
                        counter += 1
                        yticks.append(j)
                yticks_range = [l + .4 for l in range(len(yticks))]
                plt.yticks(yticks_range, yticks)
                ax.set_ylim([0, yticks_range[-1] + .4])
                plt.title("Cluster: %d" % i)
                if self.context == "notebook":
                    plt.show()
                else:
                    plt.savefig("cluster_%d%s" % (i, ".png"), bbox_inches="tight")
                    plt.close()
        else:
            cluster_distribution = pd.DataFrame(cluster_distribution).T
            cluster_distribution.index.name = "cluster_id"
            return cluster_distribution