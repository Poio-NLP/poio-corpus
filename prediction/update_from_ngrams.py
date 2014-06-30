# -*- coding: utf-8 -*-
#
# Poio Corpus
#
# Copyright (C) 2009-2014 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

# Works with Python 2 and 3, requires 64-bit Python

import sys
import os
import glob
import zipfile
import shutil
import codecs
import re
import pickle
from tempfile import mkdtemp
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import pressagio.tokenizer
import pressagio.dbconnector

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

    ngrams_dir = os.path.abspath(os.path.join("..", "build", "ngrams"))

    for iso_639_3 in config.options("LanguagesISOMap"):
        
        if arg_iso and iso_639_3 != arg_iso:
            continue

        ngram_archive = os.path.join(ngrams_dir, "{0}.zip".format(iso_639_3))
        try:
            tmp_path = mkdtemp()

            z = zipfile.ZipFile(ngram_archive)
            z.extractall(tmp_path)

            for ngram_size in [1, 2, 3]:
                print("  Parsing {0} ngrams for cardinality {1}...".format(
                    iso_639_3, ngram_size))

                ngram_file = os.path.join(tmp_path,"{0}_{1}grams.txt".format(
                    iso_639_3, ngram_size))

                if not os.path.exists(ngram_file):
                    print("  something is wrong with the archive. Exiting.")
                    sys.exit(1)

                ngram_map = dict()
                with codecs.open(ngram_file, "r", "utf-8") as f:
                    for line in f:
                        ngrams = line.split("\t")
                        if len(ngrams) != (ngram_size + 1) or "" in ngrams:
                            continue
                        ngram = tuple(ngrams[:ngram_size])
                        count = ngrams[-1]
                        ngram_map[ngram] = count

                print("  Writing result to postgres database...")
                pressagio.dbconnector.insert_ngram_map_postgres(ngram_map,
                    ngram_size, iso_639_3, append=False, create_index=True,
                    lowercase=True, normalize=True)

        finally:
            try:
                shutil.rmtree(tmp_path)
            except WindowsError:
                pass


if __name__ == "__main__":
    main(sys.argv)
