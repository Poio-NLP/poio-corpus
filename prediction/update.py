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

import requests
from config import Config

###################################### Main

def main(argv):
    config_file = file(os.path.join('..', 'config.ini'))
    config = Config(config_file)

    corpus_dir = os.path.abspath(os.path.join("..", "build", "corpus"))
    prediction_dir = os.path.join("..", "build", "prediction")
    for l in config['supported_languages']:
        
        sql_file = os.path.join(prediction_dir, "{0}.sqlite".format(
            l['iso_639_3']))

        if os.path.exists(sql_file):
            os.remove(sql_file)

        r = requests.get(
            "https://www.poio.eu/static/ignorechars/{0}.txt".format(
                l['iso_639_3']),
            verify=False)
        ignorechars = r.content.decode("utf-8")

        dictionary = []

        for f in glob.glob(
                os.path.join(corpus_dir, "{0}wiki*.zip".format(
                    l['iso_639_1']))):
            
            _, filename = os.path.split(os.path.abspath(f))
            filebasename, fileext = os.path.splitext(filename)
            language = filename[:3]

            print("Processing {0}".format(filename))

            try:
                tmp_path = mkdtemp()

                z = zipfile.ZipFile(f)
                z.extractall(tmp_path)

                text_file = os.path.join(
                    tmp_path,"{0}.txt".format(filebasename))

                # build n-gramm statistics, requires presage:
                # http://presage.sourceforge.net/
                for gram in [1, 2, 3]:
                    os.system(
                        "text2ngram -n {0} -o {1} -f sqlite -a {2}".format(
                            gram, sql_file, text_file))

                # append words to dictionary list
                doc = ""
                with codecs.open(text_file, "r", "utf-8") as f:
                    doc = f.read()
                dictionary.extend(_words_for_document(doc, ignorechars))

            finally:
                try:
                    shutil.rmtree(tmp_path)
                except:
                    pass

        # write dictionary file
        dict_file = os.path.join(prediction_dir, "{0}_dict.txt".format(
            l['iso_639_3']))
        with codecs.open(dict_file, "w", "utf-8") as f:
            f.write("\n".join(dictionary))

        # write config file
        config_template = u""
        with codecs.open("config_template.xml", "r", "utf-8") as f:
            config_template = f.read()
        config_file = os.path.join(prediction_dir, "{0}.xml".format(
            l['iso_639_3']))
        with codecs.open(config_file, "w", "utf-8") as f:
            f.write(config_template.format(l['iso_639_3']))

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
