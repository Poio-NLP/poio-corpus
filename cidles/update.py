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
import pickle
import zipfile
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

###################################### Main

def main(argv):
    arg_iso = None
    if len(argv) > 1:
        arg_iso = argv[1]

    config_file = os.path.join('..', 'config.ini')
    config = configparser.ConfigParser()
    config.read(config_file)

    processed = dict()
    processed_file = os.path.join('..', 'build', 'processed.pickle')
    if os.path.exists(processed_file):
        with open(processed_file, 'rb') as f:
            processed = pickle.load(f)
            if 'cidles' not in processed:
                processed['cidles'] = dict()

    else:
        processed['cidles'] = dict()

    for iso_639_3 in config.options("LanguagesISOMap"):
        if arg_iso and iso_639_3 != arg_iso:
            continue

        if not os.path.exists(iso_639_3):
            continue

        print("Processing corpus {0}...".format(iso_639_3))

        # create directory for clean files
        clean_dir = os.path.join(iso_639_3, "clean")
        if not os.path.exists(clean_dir):
            os.makedirs(clean_dir)

        # find text files
        corpus_files = glob.glob(os.path.join(iso_639_3, "*.txt"))

        for f in corpus_files:
            _, filename = os.path.split(os.path.abspath(f))
            filebasename, _ = os.path.splitext(filename)

            match = re.search("(.+)-(\d{8}).txt$", filename)
            fileprefix = None
            corpus_date = None
            if match:
                fileprefix = match.group(1)
                corpus_date = match.group(2)
            else:
                print "  File name does not match: {0}".format(filename)
                sys.exit(1)

            # check if we already have a clean script for this language
            clean_script = os.path.join(iso_639_3, "{0}-clean.py".format(
                    fileprefix))
            print(clean_script)
            if not os.path.exists(clean_script):
                print("  No clean script found. Skipping.")
                continue
            clean_file = os.path.join(clean_dir, filename)

            # check if there is already build for this corpus
            output_file = os.path.join(
                '..', 'build', 'corpus', "{0}.zip".format(fileprefix))

            if iso_639_3 in processed['cidles'] and \
                    int(processed['cidles'][iso_639_3]) >= int(corpus_date) and \
                    os.path.exists(output_file):
                print "  Corpus already processed, skipping."
                continue

            # Calling clean scripts
            print("Cleaning...")
            os.system("{0} {1} {2} {3}".format(
                sys.executable, clean_script, f, clean_file))

            # Zipping
            print("Zipping...")
            myzip = zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED)
            myzip.write(clean_file, os.path.basename(clean_file))
            myzip.write("LICENSE.cidles", "LICENSE")
            myzip.close()

            processed['cidles'][iso_639_3] = corpus_date
            with open(processed_file, 'wb') as f:
                pickle.dump(processed, f)

if __name__ == "__main__":
    main(sys.argv)
