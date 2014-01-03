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
import pickle
import zipfile
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import requests
from BeautifulSoup import BeautifulSoup

import helpers

###################################### Main

def main(argv):
    arg_iso = None
    if len(argv) > 1:
        arg_iso = argv[1]

    script_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_path)

    config_file = os.path.join('..', 'config.ini')
    config = configparser.ConfigParser()
    config.read(config_file)

    processed = dict()
    processed_file = os.path.join('..', 'build', 'processed.pickle')
    if os.path.exists(processed_file):
        with open(processed_file, 'rb') as f:
            processed = pickle.load(f)

    if 'wikipedia' not in processed:
        processed['wikipedia'] = dict()


    for iso_639_3 in config.options("LanguagesISOMap"):
        if arg_iso and iso_639_3 != arg_iso:
            continue

        iso_639_1 = config.get("LanguagesISOMap", iso_639_3)
        wiki_prefix = "{0}wiki".format(iso_639_1)
        new_wiki_prefix = "{0}wiki".format(iso_639_3)

        print("Processing wikipedia {0} -> {1}...".format(iso_639_1, iso_639_3))

        # check if we already have a clean script for this language
        if not os.path.exists(os.path.join(new_wiki_prefix, "clean2.py")):
            print("No clean script found. Skipping.")
            continue

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
        output_file = os.path.join(
            '..', 'build', 'corpus', "{0}.zip".format(new_wiki_prefix))

        if iso_639_3 in processed['wikipedia'] and \
                int(processed['wikipedia'][iso_639_3]) >= int(wiki_date) and \
                os.path.exists(output_file):
            print "  Wikipedia already processed, skipping."
            continue

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
       
        os.system("{0} {1}/clean2.py {2} {3}".format(
            sys.executable,
            new_wiki_prefix,
            os.path.join(
                new_wiki_prefix, "{0}_cleaned1.xml".format(new_wiki_prefix)),
            os.path.join(
                new_wiki_prefix, "{0}_cleaned2.xml".format(new_wiki_prefix))))

        os.system("{0} clean3.py {1} {2}".format(
            sys.executable,
            os.path.join(
                new_wiki_prefix, "{0}_cleaned2.xml".format(new_wiki_prefix)),
            os.path.join(
                new_wiki_prefix, "{0}_cleaned3.xml".format(new_wiki_prefix))))

        print("Converting to GrAF...")
        os.system("{0} to_graf.py {1} {2}".format(
            sys.executable,
            os.path.join(
                new_wiki_prefix, "{0}_cleaned3.xml".format(new_wiki_prefix)),
            os.path.join(
                new_wiki_prefix, "{0}-{1}.hdr".format(
                    new_wiki_prefix, wiki_date))))

        # Zipping
        print("Zipping...")
        files = [
            os.path.join(
                new_wiki_prefix, "{0}-{1}.hdr".format(
                    new_wiki_prefix, wiki_date)),
            os.path.join(
                new_wiki_prefix, "{0}-{1}.txt".format(
                    new_wiki_prefix, wiki_date)),
            os.path.join(
                new_wiki_prefix, "{0}-{1}-doc.xml".format(
                    new_wiki_prefix, wiki_date))
        ]
        myzip = zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED)
        for f in files:
            myzip.write(f, os.path.basename(f))
        myzip.write("LICENSE.wikipedia", "LICENSE")
        myzip.close()

        processed['wikipedia'][iso_639_3] = wiki_date
        with open(processed_file, 'wb') as f:
            pickle.dump(processed, f)

if __name__ == "__main__":
    main(sys.argv)