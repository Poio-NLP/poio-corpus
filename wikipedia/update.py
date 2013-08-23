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
    html_page = urllib2.urlopen(page)
    soup = BeautifulSoup(html_page)
    all_links = soup('a')
    dump_link = None
    wiki_date = None
    for l in all_links:
        match = re.match(wiki_name + "-(\d{8})-pages-articles.xml.bz2", l.string)
        if match:
            wiki_date = match.group(1)
            dump_link = urlparse.urljoin(page, l['href'])
            break

    if not dump_link:
        print("Could not find dump link for {0}.".format(wiki_name))
        sys.exit(1)

    print("Downloading {0}...".format(dump_link))
    file_name = dump_link.split('/')[-1]
    file_path = os.path.join(wiki_name, file_name)
    if not os.path.exists(file_path):
        r = requests.get(dump_link)
        with open(file_path, "wb") as f:
            f.write(r.content)

    os.system("{0} WikiExtractor.py -w -f tanl {1} {2}/extracted".format(
        sys.executable,
        file_path,
        wiki_name))

    # Concatenate output files
    filenames = glob.glob("{0}/extracted/*.raw".format(wiki_name))
    with codecs.open(os.path.join(
            wiki_name, "{0}.xml".format(wiki_name)), 'w', 'utf-8') as outfile:
        for fname in filenames:
            with codecs.open(fname, "r", "utf-8") as infile:
                for line in infile:
                    outfile.write(line)

    # Calling clean scripts
    print("Cleaning...")
    os.system("{0} clean.py {1} {2}".format(
        sys.executable,
        os.path.join(wiki_name, "{0}.xml".format(wiki_name)),
        os.path.join(wiki_name, "{0}_cleaned1.xml".format(wiki_name))))

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
    myzip.close()

    print
