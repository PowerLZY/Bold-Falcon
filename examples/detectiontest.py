import sys
sys.path.append("..")

from modules.detection.instance import Instance
from modules.detection.loader import Loader
from modules.processing.cuckooml import ML
from pprint import pprint

# The first stage is to load the data from the directory holding all the JSONs
loader = Loader()
loader.load_binaries("../sample_data/dict")

# Then we extract all the relevant information from the loaded samples.
simple_features_dict = loader.get_simple_features()
features_dict = loader.get_features()
"""
{simple_features_dict['165']:
u'injection_runpe': u'Executed a process and injected code into it, probably while unpacking', 
u'worm_renocide': u'Creates known Renocide Worm files, registry keys and/or mutexes', 
u'pe_features': u'The executable has PE anomalies (could be a false positive)', 
u'raises_exception': u'One or more processes crashed', 
u'dumped_buffer': u'One or more potentially interesting buffers were extracted, these generally contain injected code, configuration data, etc.', 
u'antisandbox_productid': u'Retrieves Windows ProductID, probably to fingerprint the sandbox',
u'antivirus_virustotal': u'File has been identified by at least one AntiVirus on VirusTotal as malicious', 
u'allocates_rwx': u'Allocates read-write-execute memory (usually to unpack itself)',
 u'packer_upx': u'The executable is compressed using UPX'}
"""
labels_dict = loader.get_labels()

# Now that all the needed information are at hand we create a cuckooml Machine Learning instance
# and inject therein all these information.
# ml = ML(context="notebook")
ml = ML()
ml.load_simple_features(simple_features_dict)
ml.load_features(features_dict)
ml.load_labels(labels_dict)

# Once loaded into ML class the data is reformated into Pandas DataFrame object
# therefore it is easy to manipulate and use it with variety of machine learning algorithms.
simple_features = ml.simple_features
features = ml.features
labels = ml.labels
