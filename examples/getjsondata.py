# Copyright (C) 2010-2013 Claudio Guarnieri.
# Copyright (C) 2014-2016 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

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