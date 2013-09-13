# -*- coding: utf-8 -*-
#
# Poio Corpus
#
# Copyright (C) 2009-2013 Poio Project
# Author: Eva Schinzel
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

# Script in order to prepare languages for the application of the clean2.py-script, 
# i.e. automatically downloading dump, running first clean script.

# If you run this script without additional arguments (just prepare.py), 
# it prepares all languages that have no cleaned2.xml-file yet.

# If you specify additional arguments (e.g. prepare.py barwiki sawiki), 
# it prepares the languages being referred to by these arguments
# unless there already exists a clean2.xml-file for one of them.
# In this case this particular language is excluded from the preparation. 

import os
import sys
import re
import glob
import codecs
import urllib2
import urlparse
import requests
import helpers
from BeautifulSoup import BeautifulSoup

languages = os.walk('.').next()[1]

#list to collect all the languages to prepare
current_languages = [] 

if len(sys.argv) == 1: #if no language is specified in command line
    for l in languages: #iterates over existing directories
        cleaned2_path = os.path.join(l, "{0}_cleaned2.xml".format(l)) #path to cleaned2.xml-file
        if not os.path.exists(cleaned2_path): #if there is no cleaned2.xml-file for language yet
            current_languages.append(l) #adds language to list of languages to prepare
else: #if one ore more language is specified in command line
    for i in range(1, len(sys.argv)): #iterates over argv while excluding argv[0] (=> names of specified languages)
        if sys.argv[i] in languages: #checks if there exists a directory named after specified language
            cleaned2_path = os.path.join(sys.argv[i], "{0}_cleaned2.xml".format(sys.argv[i])) #see above...
            if not os.path.exists(cleaned2_path): #see above...
                current_languages.append(sys.argv[i]) #see above...
        else: #in case there is no directory named after specified language
            print("A directory named {0} is required in order to prepare this language. (Also {0} has to be a wikiname (e.g. barwiki, sawiki, ...).)".format(sys.argv[i]))

            
#further steps only for languages that have not been prepared yet            
languages = current_languages 

if len(languages) == 0:
    print("There are no languages to prepare that match your request...")
    sys.exit(1)
else: 
    print("Preparing the following languages: {0} ...".format(languages))


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

    helpers.wikipedia_extractor(file_path, wiki_name)

    # Concatenate output files
    filenames = glob.glob(os.path.join(wiki_name, "extracted", "*.raw"))
    with codecs.open(os.path.join(
            wiki_name, "{0}.xml".format(wiki_name)), 'w', 'utf-8') as outfile:
        for fname in filenames:
            with codecs.open(fname, "r", "utf-8") as infile:
                for line in infile:
                    outfile.write(line)

    # Calling first clean script
    print("Cleaning...")
    os.system("{0} clean.py {1} {2}".format(
        sys.executable,
        os.path.join(wiki_name, "{0}.xml".format(wiki_name)),
        os.path.join(wiki_name, "{0}_cleaned1.xml".format(wiki_name))))