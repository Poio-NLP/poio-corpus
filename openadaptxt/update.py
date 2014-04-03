# -*- coding: utf-8 -*-
#
# Poio Corpus
#
# Copyright (C) 2009-2014 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

# Works with Python 2 and 3, requires 64-bit Python
# This script uses the data from the openadaptxt project to update and clean
# the language model

import sys
import os
import glob
import zipfile
import shutil
import codecs
import re
import collections
import pickle
from tempfile import mkdtemp
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import pressagio.dbconnector

re_line_end = re.compile(" ,$")

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

    if 'openadaptxt' not in processed:
        processed['openadaptxt'] = dict()

    corpus_dir = os.path.abspath(os.path.join("..", "build", "openadaptxt"))
    prediction_dir = os.path.join("..", "build", "prediction")

    for iso_639_3 in config.options("LanguagesISOMap"):

        if arg_iso and iso_639_3 != arg_iso:
            continue

        sql_file = os.path.join(prediction_dir, "{0}.sqlite".format(
            iso_639_3))

        corpus_archive = os.path.join(corpus_dir, "{0}.zip".format(iso_639_3))
        if not os.path.exists(corpus_archive):
            continue

        #corpus_date = os.path.getmtime(corpus_archive)

        if not arg_iso and iso_639_3 in processed['openadaptxt'] and \
                iso_639_3 in processed['prediction'] and \
                int(processed['openadaptxt'][iso_639_3]) >= \
                int(processed['prediction'][iso_639_3]):
            print "  Corpus files already processed, skipping."
            continue

        _, filename = os.path.split(os.path.abspath(corpus_archive))
        filebasename, _ = os.path.splitext(filename)

        print("Processing {0}".format(filename))

        try:
            tmp_path = mkdtemp()

            z = zipfile.ZipFile(corpus_archive)
            z.extractall(tmp_path)

            corpus_files = glob.glob(os.path.join(
                tmp_path,"{0}*_corpus.txt".format(filebasename)))

            if len(corpus_files) != 1:
                print("  something is wrong with the archive. Exiting.")
                sys.exit(1)

            corpus_file = corpus_files[0]

            # get the data in the file
            ngrams = [collections.defaultdict(int),
                collections.defaultdict(int),
                collections.defaultdict(int)]
            print("  Parsing corpus file {0}...".format(corpus_file))
            with codecs.open(corpus_file, "r", "utf-16") as f:
                for line in f:
                    # remove comma and whitespace
                    ngram = re_line_end.sub("", line).split()
                    if len(ngram) <= 3:
                        ngrams[len(ngram)-1][tuple(ngram)] += 1

            for ngram_size, ngram_map in enumerate(ngrams):
                print("  Adding cardinality {0}...".format(ngram_size+1))

                ngram_map = ngrams[ngram_size]

                print("  Writing result to sqlite database...")
                pressagio.dbconnector.insert_ngram_map_sqlite(ngram_map,
                    ngram_size+1, sql_file, append=True, create_index=True)

                print("  Writing result to postgres database...")
                pressagio.dbconnector.insert_ngram_map_postgres(ngram_map,
                    ngram_size+1, iso_639_3, append=True, create_index=True,
                    lowercase=True, normalize=True)

            # Now filter the ngrams in the DB. We use the "_inclusion" file
            # as a dictionary and delete all ngrams that contain words that
            # are not in the dictionary
            inclusion_files = glob.glob(os.path.join(
                tmp_path,"{0}*_inclusion.txt".format(filebasename)))

            if len(inclusion_files) != 1:
                print("  something is wrong with the archive. Exiting.")
                sys.exit(1)

            inclusion_file = inclusion_files[0]

            # get the data in the file
            dictionary = set()
            print("  Parsing inclusion file {0}...".format(inclusion_file))
            with codecs.open(inclusion_file, "r", "utf-16") as f:
                for line in f:
                    dictionary.add(line.strip())

            for ngram_size in [1, 2, 3]:
                pressagio.dbconnector.filter_ngrams_postgres(dictionary,
                    ngram_size, iso_639_3)

        finally:
            try:
                shutil.rmtree(tmp_path)
            except WindowsError:
                pass

        processed['openadaptxt'][iso_639_3] = processed['prediction'][iso_639_3]
        with open(processed_file, 'wb') as f:
            pickle.dump(processed, f)


if __name__ == "__main__":
    main(sys.argv)
