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
import optparse
import datetime
import dateutil.parser
from zipfile import ZipFile
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import requests

def main(argv):
    usage = "usage: %prog [options]"
    parser = optparse.OptionParser(usage=usage, version="%prog 0.1")
    parser.add_option("-n", "--newer", action="store_true", dest="newer",
        default=False,
        help="Only download files when they are newer than local files")
    parser.add_option("-f", "--force", action="store_true", dest="force",
        default=False, help="Overwrite existing local files")
    (options, _) = parser.parse_args()

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
        date = contents.find("{http://s3.amazonaws.com/doc/2006-03-01/}LastModified")
        server_date = dateutil.parser.parse(date.text)

        target_path = os.path.join(static_data_path, subdir, filename)
        print("Processing file {0}...".format(filename))
        download = False
        if options.force:
            download = True
        elif not os.path.exists(target_path):
            download = True
        if not options.newer and os.path.exists(target_path):
            print("  file already exists, skipping.")
        elif options.newer and os.path.exists(target_path):
            local_date = datetime.datetime.fromtimestamp(
                os.path.getmtime(target_path))
            server_date = server_date.replace(tzinfo=None)
            if local_date < server_date:
                download = True
            else:
                print("  local file found and is up-to-date, skipping.")

        if download:
            download_url = url + "/" + file_url
            print("  downloading from {0}...".format(download_url))
            r = requests.get(download_url, stream=True)
            with open(target_path, "wb") as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)

        if filename.endswith(".sqlite.zip"):
            print("  unzipping file...")
            myzip = ZipFile(target_path, "r")
            myzip.extractall(os.path.join(static_data_path, subdir))
            myzip.close()

if __name__ == "__main__":
    main(sys.argv)