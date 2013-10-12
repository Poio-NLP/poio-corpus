# -*- coding: utf-8 -*-
#
# Poio Corpus
#
# Copyright (C) 2009-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

import os
import sys
import urllib2
import urlparse
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import requests

def main(argv):
    url = "http://s3.amazonaws.com/poiocorpus"
    xml_page = urllib2.urlopen(url)
    tree = ET.ElementTree(file=xml_page)
    root = tree.getroot()

    static_data_path = os.path.join("src", "main", "static")

    for contents in root.findall(
            "{http://s3.amazonaws.com/doc/2006-03-01/}Contents"):
        key = contents.find("{http://s3.amazonaws.com/doc/2006-03-01/}Key")
        file_url = key.text
        subdir, filename = file_url.split("/")

        target_path = os.path.join(static_data_path, subdir, filename)
        #print("Checking if file {0} exists...".format(target_path))
        #if not os.path.exists(target_path):
        download_url = url + "/" + file_url
        print("  downloading from {0}...".format(download_url))
        r = requests.get(download_url, stream=True)
        with open(target_path, "wb") as f:
            f.write(r.content)

if __name__ == "__main__":
    main(sys.argv)