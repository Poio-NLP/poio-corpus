# -*- coding: utf-8 -*-
#
# Poio Corpus
#
# Copyright (C) 2009-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

import sys
import os
import glob
import zipfile
import shutil
import codecs
import re
from tempfile import mkdtemp
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import pressagio.tokenizer
import pressagio.dbconnector

###################################### Main

def main(argv):
    config_file = os.path.join('..', 'config.ini')
    config = configparser.ConfigParser()
    config.read(config_file)

    corpus_dir = os.path.abspath(os.path.join("..", "build", "corpus"))
    prediction_dir = os.path.join("..", "build", "prediction")
    for iso_639_3 in config.options("LanguagesISOMap"):
        
        sql_file = os.path.join(prediction_dir, "{0}.sqlite".format(
            iso_639_3))

        if os.path.exists(sql_file):
            os.remove(sql_file)

        separators_file = os.path.join(
            "..", "build", "separators", "allchars.txt")
        s_f = codecs.open(separators_file, "r", "utf-8")
        separators = s_f.read()
        s_f.close()

        dictionary = []

        for f in glob.glob(
                os.path.join(corpus_dir, "{0}wiki*.zip".format(
                    iso_639_3))):
            
            _, filename = os.path.split(os.path.abspath(f))
            filebasename, _ = os.path.splitext(filename)

            print("Processing {0}".format(filename))

            try:
                tmp_path = mkdtemp()

                z = zipfile.ZipFile(f)
                z.extractall(tmp_path)

                text_file = os.path.join(
                    tmp_path,"{0}.txt".format(filebasename))

                # build n-gramm statistics, requires pressagio:
                # http://github.com/cidles/pressagio
                for ngram_size in [1, 2, 3]:
                    print("  Parsing {0} for cardinality {1}...".format(
                        text_file, ngram_size))
                    ngram_map = pressagio.tokenizer.forward_tokenize_file(
                        text_file, ngram_size)

                    print("  Writing result to {0}...".format(sql_file))
                    pressagio.dbconnector.insert_ngram_map(ngram_map,
                        ngram_size, sql_file, False)

                    #os.system(
                    #    "text2ngram -n {0} -o {1} -f sqlite -a {2}".format(
                    #        gram, sql_file, text_file))

                # append words to dictionary list
                doc = ""
                with codecs.open(text_file, "r", "utf-8") as f:
                    doc = f.read()
                dictionary.extend(_words_for_document(doc, separators))

            finally:
                try:
                    shutil.rmtree(tmp_path)
                except:
                    pass

        # write dictionary file
        #dict_file = os.path.join(prediction_dir, "{0}_dict.txt".format(
        #    iso_639_3))
        #with codecs.open(dict_file, "w", "utf-8") as f:
        #    f.write("\n".join(dictionary))

        # write config file
        config_template = u""
        with codecs.open("config_template.ini", "r", "utf-8") as f:
            config_template = f.read()
        config_file = os.path.join(prediction_dir, "{0}.ini".format(
            iso_639_3))
        with codecs.open(config_file, "w", "utf-8") as f:
            f.write(config_template.format(iso_639_3))

###################################### Helpers

def _words_for_document(doc, ignorechars):
    re_ignore_chars = re.compile(u"[{0}]".format(ignorechars))
    words = doc.split()
    words2 = set()

    for w in words:
        w = re_ignore_chars.sub("", w)

        if w == "":
            continue

        words2.add(w)

    return words2


if __name__ == "__main__":
    main(sys.argv)
