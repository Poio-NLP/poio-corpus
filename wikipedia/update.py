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
import re
import glob
import codecs
import urllib2
import urlparse
import zipfile
import helpers
import requests
from BeautifulSoup import BeautifulSoup

languages = os.walk('.').next()[1]

url = "http://dumps.wikimedia.org/backup-index.html"
html_page = urllib2.urlopen(url)
soup = BeautifulSoup(html_page)

lang_pages = [(link.string, urlparse.urljoin(url, link['href']))
                for l in languages
                    for link in soup('a')
                        if link.string == l]

for wiki_name, page in lang_pages:
    wiki_date, dump_link = helpers.dump_link(wiki_name, page)

    if not dump_link:
        print("Could not find dump link for {0}.".format(wiki_name))
        sys.exit(1)

    print("Downloading {0}...".format(dump_link))
    file_path = helpers.download_dump(dump_link, wiki_name)
   
    
    helpers.wikipedia_extractor(file_path, wiki_name)

    # Concatenate output files
    helpers.concatenate(wiki_name)

    # Calling clean scripts
    print("Cleaning...")
    helpers.clean_1(wiki_name)   
   

    os.system("{0} {1}/clean2.py {2} {3}".format(
        sys.executable,
        wiki_name,
        os.path.join(wiki_name, "{0}_cleaned1.xml".format(wiki_name)),
        os.path.join(wiki_name, "{0}_cleaned2.xml".format(wiki_name))))

    os.system("{0} clean3.py {1} {2}".format(
        sys.executable,
        os.path.join(wiki_name, "{0}_cleaned2.xml".format(wiki_name)),
        os.path.join(wiki_name, "{0}_cleaned3.xml".format(wiki_name))))

    print("Converting to GrAF...")
    os.system("{0} to_graf.py {1} {2}".format(
        sys.executable,
        os.path.join(wiki_name, "{0}_cleaned3.xml".format(wiki_name)),
        os.path.join(wiki_name, "{0}-{1}.hdr".format(wiki_name, wiki_date))))

    # Zipping
    print("Zipping...")
    files = [
        os.path.join(wiki_name, "{0}-{1}.hdr".format(wiki_name, wiki_date)),
        os.path.join(wiki_name, "{0}-{1}.txt".format(wiki_name, wiki_date)),
        os.path.join(wiki_name, "{0}-{1}-doc.xml".format(wiki_name, wiki_date))
    ]
    myzip = zipfile.ZipFile(os.path.join(
        '..', 'build', 'corpus', "{0}-{1}.zip".format(wiki_name, wiki_date)), 
        'w', zipfile.ZIP_DEFLATED)
    for f in files:
        myzip.write(f, os.path.basename(f))
    myzip.write("LICENSE.wikipedia", "LICENSE")
    myzip.close()

    print
