# -*- coding: utf-8 -*-
#
# Poio Corpus
#
# Copyright (C) 2009-2015 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

import os
import sys
import glob
import codecs
import zipfile
import bz2
import re
import urllib.parse
import subprocess

import requests
from bs4 import BeautifulSoup

def dump_link(wiki_name, page):
    html_page = requests.get(page)
    soup = BeautifulSoup(html_page.content)
    all_links = soup('a')
    for l in all_links:
        match = re.match(
            wiki_name + "-(\d{8})-pages-articles.xml.bz2", l.string)
        if match:
            wiki_date = match.group(1)
            dump_link = urllib.parse.urljoin(page, l['href'])
            return wiki_date, dump_link
    return None, None
            
def download_dump(dump_link, wiki_name, new_wiki_name):
    file_name = dump_link.split('/')[-1]
    file_path = os.path.join(new_wiki_name, file_name)
    if not os.path.exists(file_path):
        r = requests.get(dump_link)
        with open(file_path, "wb") as f:
            f.write(r.content)
    return file_path

def wikipedia_extractor(file_path, new_wiki_name):
    out = None; err = None
    file_path_uncompressed = os.path.splitext(file_path)[0]
    with bz2.open(file_path, mode="rb") as f, codecs.open(file_path_uncompressed, "w", "utf-8") as o:
        o.write(f.read().decode("utf-8"))

    with open(file_path_uncompressed, "rb") as f:
        proc = subprocess.Popen([
            sys.executable,
            "WikiExtractor.py",
            "-b", "200000000000",
            "-o", os.path.join(new_wiki_name, "extracted")
            ], stdout=subprocess.PIPE, stdin=f)
        (out, err) = proc.communicate()
    return (out, err)
        
        
def concatenate(new_wiki_name):
    filenames = glob.glob(os.path.join(new_wiki_name, "extracted", "AA", "wiki_*"))
    with codecs.open(os.path.join(
            new_wiki_name, "{0}.xml".format(new_wiki_name)), 'w', 'utf-8')\
            as outfile:
        for fname in filenames:
            with codecs.open(fname, "r", "utf-8") as infile:
                for line in infile:
                    outfile.write(line)
                    
def clean_1(new_wiki_name):
    os.system("{0} clean.py {1} {2}".format(
        sys.executable,
        os.path.join(new_wiki_name, "{0}.xml".format(new_wiki_name)),
        os.path.join(new_wiki_name, "{0}_cleaned1.xml".format(new_wiki_name))))

