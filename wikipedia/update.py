# -*- coding: utf-8 -*-
#
# Poio Corpus
#
# Copyright (C) 2009-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

import os
import re
import xml.etree.ElementTree as ET
import urllib2
import urlparse

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
    for l in all_links:
        if re.match(wiki_name + "-\d{8}-pages-articles.xml.bz2", l.string):
            dump_link = urlparse.urljoin(page, l['href'])
            break

    if not dump_link:
        print("Could not find dump link for {0}.".format(wiki_name))
        sys.exit(1)

    print("Downloading {0}...".format(dump_link))
    r = requests.get(dump_link)
    file_name = dump_link.split('/')[-1]
    with open(os.path.join(wiki_name, file_name), "wb") as f:
        f.write(r.content)

#tree = ET.parse('barwiki-cleaned.xml')
#root = tree.getroot()