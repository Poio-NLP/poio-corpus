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
import zipfile
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import requests
from BeautifulSoup import BeautifulSoup

import helpers

languages = os.walk('.').next()[1]
#list to collect all the languages to prepare
current_languages = [] 

#if no language is specified in command line
if len(sys.argv) == 1: 
    for l in languages: 
        #path to cleaned2.xml-file
        cleaned2_path = os.path.join(l, "{0}_cleaned2.xml".format(l)) 
        if not os.path.exists(cleaned2_path): 
            current_languages.append(l) 
#if one ore more language is specified in command line
else: 
    #iterates over argv while excluding argv[0] (=> names of specified languages)
    for i in range(1, len(sys.argv)): 
        #checks if there exists a directory named after specified language
        if sys.argv[i] in languages: 
            cleaned2_path = os.path.join(sys.argv[i], "{0}_cleaned2.xml".format(sys.argv[i])) 
            if not os.path.exists(cleaned2_path):
                current_languages.append(sys.argv[i]) 
        #in case there is no directory named after specified language
        else: 
            print("A directory named {0} is required in order to prepare this language. (Also {0} has to be a wikiname (e.g. barwiki, sawiki, ...).)".format(sys.argv[i]))

            
#further steps only for languages that have not been prepared yet            
languages = current_languages 

if len(languages) == 0:
    print("There are no languages to prepare that match your request...")
    sys.exit(1)
else: 
    print("Preparing the following languages: {0} ...".format(languages))


    
def main(argv):
    config_file = os.path.join('..', 'config.ini')
    config = configparser.ConfigParser()
    config.read(config_file)

    for iso_639_3 in config.options("LanguagesISOMap"):
        iso_639_1 = config.get("LanguagesISOMap", iso_639_3)
        wiki_prefix = "{0}wiki".format(iso_639_1)
        new_wiki_prefix = "{0}wiki".format(iso_639_3)

        # finds out if the language currently dealt with in the for loop is part of the list of languages to prepare
        # this also means: iso_639_3 code of language to prepare has to be in config file as well as it has to be the folder name
        if not new_wiki_prefix in languages:
            print("Skipping {0}, since it does not belong to the languages to prepare".format(new_wiki_prefix))
            continue
        
        print("Processing wikipedia {0} -> {1}...".format(iso_639_1, iso_639_3))


        url = "http://dumps.wikimedia.org/backup-index.html"
        html_page = urllib2.urlopen(url)
        soup = BeautifulSoup(html_page)

        page = None
        for link in soup('a'):
            if link.string == wiki_prefix:
                page = urlparse.urljoin(url, link['href'])

        # get the link for the dump file
        wiki_date, dump_link = helpers.dump_link(wiki_prefix, page)

        if not dump_link:
            sys.stderr.write("Could not find dump link. Abort.")
            sys.exit(1)

        # check if there is already build for this Wikipedia dump
        #output_file = os.path.join(
            #'..', 'build', 'corpus', "{0}.zip".format(new_wiki_prefix,
                #wiki_date))
        #if os.path.exists(output_file):
        #    print("Output file already exists. Skipping.")
        #    continue

        # download dump
        print("Downloading {0}...".format(dump_link))
        file_path = helpers.download_dump(dump_link, wiki_prefix,
            new_wiki_prefix)
       
        print("Running WikiExtractor...")
        helpers.wikipedia_extractor(file_path, new_wiki_prefix)

        # Concatenate output files
        helpers.concatenate(new_wiki_prefix)

        # Calling clean scripts
        print("Cleaning...")
        helpers.clean_1(new_wiki_prefix)          
    
if __name__ == "__main__":
    main(sys.argv)     