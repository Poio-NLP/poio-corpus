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
import glob
import codecs
import zipfile
import requests
import re
import urllib2
import urlparse
from BeautifulSoup import BeautifulSoup

def dump_link(wiki_name, page):
    html_page = urllib2.urlopen(page)
    soup = BeautifulSoup(html_page)
    all_links = soup('a')
    for l in all_links:
        match = re.match(wiki_name + "-(\d{8})-pages-articles.xml.bz2", l.string)
        if match:
            wiki_date = match.group(1)
            dump_link = urlparse.urljoin(page, l['href'])
            return wiki_date, dump_link
    return None, None
            
def download_dump(dump_link, wiki_name):
    file_name = dump_link.split('/')[-1]
    file_path = os.path.join(wiki_name, file_name)
    if not os.path.exists(file_path):
        r = requests.get(dump_link)
        with open(file_path, "wb") as f:
            f.write(r.content)
    return file_path

def wikipedia_extractor(file_path, wiki_name):
    os.system("{0} WikiExtractor.py -w -f tanl {1} {2}/extracted".format(
        sys.executable,
        file_path,
        wiki_name))
        
        
def concatenate(wiki_name):
    filenames = glob.glob(os.path.join(wiki_name, "extracted", "*.raw"))
    with codecs.open(os.path.join(
            wiki_name, "{0}.xml".format(wiki_name)), 'w', 'utf-8') as outfile:
        for fname in filenames:
            with codecs.open(fname, "r", "utf-8") as infile:
                for line in infile:
                    outfile.write(line)
                    
def clean_1(wiki_name):
    os.system("{0} clean.py {1} {2}".format(
        sys.executable,
        os.path.join(wiki_name, "{0}.xml".format(wiki_name)),
        os.path.join(wiki_name, "{0}_cleaned1.xml".format(wiki_name))))

