# -*- coding: utf-8 -*-
#
# Poio Corpus
#
# Copyright (C) 2009-2014 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

from __future__ import unicode_literals

import os
import sys
import pickle
import codecs
import collections
import zipfile
import shutil
from tempfile import mkdtemp
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import pressagio.dbconnector

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

    if 'ngrams' not in processed:
        processed['ngrams'] = dict()

    ngrams_dir = os.path.join("..", "build", "ngrams")
    for iso_639_3 in config.options("LanguagesISOMap"):
        
        if arg_iso and iso_639_3 != arg_iso:
            continue

        print("Processing {0}...".format(iso_639_3))

        if not arg_iso and iso_639_3 in processed['ngrams'] and \
                iso_639_3 in processed['prediction'] and \
                int(processed['ngrams'][iso_639_3]) >= \
                int(processed['prediction'][iso_639_3]):
            print "  N-grams already exported, skipping."
            continue

        files = []

        tmp_path = mkdtemp()

        print("  Exporting n-grams...")
        sql = pressagio.dbconnector.PostgresDatabaseConnector(iso_639_3, 1)
        sql.open_database()
        chars = collections.defaultdict(int)
        for ngram_size in [3, 2, 1]:
            sql.cardinality = ngram_size
            ngrams = { tuple(u[0:-1]): u[-1] for u in sql.ngrams(True) }

            ngrams_filename =  "{0}_{1}grams.txt".format(
                iso_639_3, ngram_size)
            ngrams_file = codecs.open(
                os.path.join(tmp_path, ngrams_filename), "w", "utf-8")

            for u in reversed(sorted(ngrams.items(), key=lambda x: x[1])):
                ngrams_file.write("{0}\t{1}\n".format("\t".join(u[0]), u[1]))
                if ngram_size == 1:
                    for ch in u[0][0]:
                        chars[ch] += 1

            ngrams_file.close()
            files.append(ngrams_filename)

        sql.close_database()

        chars_filename = "{0}_chars.txt".format(
            iso_639_3)
        chars_file = codecs.open(os.path.join(tmp_path, chars_filename),
            "w", "utf-8")
        for ch in reversed(sorted(chars.items(), key=lambda x: x[1])):
            chars_file.write("{0}\t{1}\n".format(ch[0], ch[1]))
        chars_file.close()
        files.append(chars_filename)

        print("  Zipping")
        myzip = zipfile.ZipFile(
            os.path.join(ngrams_dir, "{0}.zip".format(iso_639_3)), 'w',
            zipfile.ZIP_DEFLATED, True)
        for f in files:
            myzip.write(os.path.join(tmp_path, f), f)
        myzip.close()

        try:
            shutil.rmtree(tmp_path)
        except WindowsError:
            pass

        processed['ngrams'][iso_639_3] = processed['prediction'][iso_639_3]
        with open(processed_file, 'wb') as f:
            pickle.dump(processed, f)


if __name__ == "__main__":
    main(sys.argv)