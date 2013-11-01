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
import glob
import re
import io
import math
import codecs
import zipfile
import shutil
import pickle
from tempfile import mkdtemp
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import numpy as np
import scipy.sparse
from sparsesvd import sparsesvd
import graf

def main(argv):
    config_file = os.path.join('..', 'config.ini')
    config = configparser.ConfigParser()
    config.read(config_file)

    semantics_dir = os.path.join("..", "build", "semantics")
    corpus_dir = os.path.join("..", "build", "corpus")

    for iso_639_3 in config.options("LanguagesISOMap"):
        for f in glob.glob(
                os.path.join(corpus_dir, "{0}wiki.zip".format(
                    iso_639_3))):

            _, filename = os.path.split(os.path.abspath(f))
            filebasename, _ = os.path.splitext(filename)

            print("Processing {0}".format(filename))

            stopwords_file = os.path.join("..", "build", "stopwords",
                "{0}.txt".format(iso_639_3))
            if not os.path.exists(stopwords_file):
                print("  No stopwords file found, skipping.")
                continue
            s_f = codecs.open(stopwords_file, "r", "utf-8")
            stopwords = s_f.read().split()
            s_f.close()

            separators_file = os.path.join(
                "..", "build", "separators", "allchars.txt")
            s_f = codecs.open(separators_file, "r", "utf-8")
            separators = s_f.read()
            s_f.close()

            try:
                tmp_path = mkdtemp()

                z = zipfile.ZipFile(f)
                z.extractall(tmp_path)

                gp = graf.GraphParser()
                header_files = glob.glob(os.path.join(
                    tmp_path,"{0}*.hdr".format(filebasename)))
                g = gp.parse(header_files[0])

                text_files = glob.glob(os.path.join(
                    tmp_path,"{0}*.txt".format(filebasename)))
                text = codecs.open(text_files[0], "r", "utf-8")
                txt = text.read()
                text.close()

                documents = list()
                for n in g.nodes:
                    if n.id.startswith("doc..") and len(n.links) > 0 and \
                            len(n.links[0]) > 0:
                        doc = txt[n.links[0][0].start:n.links[0][0].end]
                        documents.append(doc)

            finally:
                try:
                    shutil.rmtree(tmp_path)
                except WindowsError:
                    pass


            print("  Pre-processing...")

            re_ignore_chars = re.compile(u"[{0}]".format(separators))
            def _words_for_document(doc):
                words = doc.split()
                words2 = list()

                for w in words:
                    w = re_ignore_chars.sub("", w.lower())

                    if not w or w in stopwords:
                        continue
                    
                    words2.append(w)

                return words2

            wdict = {}
            for i, d in enumerate(documents):
                for w in _words_for_document(d):
                    if w in wdict:
                        wdict[w].append(i)
                    else:
                        wdict[w] = [i]

            # Which 1000 words occur most often?
            top_words = [k for k in sorted(wdict, key=lambda k: len(
                wdict[k]), reverse=True)][:1000]
            # get all words that appear at least 3 times and sort them
            keys = [k for k in wdict.keys() if len(wdict[k]) > 2]
            keys.sort()
            keys_indices = { w: i for i, w in enumerate(keys) }
            # create and empty count matrix
            A = np.zeros([len(keys), len(top_words)])

            print("  Processing...")

            for d in documents:
                words = _words_for_document(d)
                len_words = len(words) - 1
                for i, w in enumerate(words):
                    if w not in keys_indices:
                        continue
                    start = i - 15
                    if i < 0:
                        start = 0
                    end = len_words
                    if end > i + 15:
                        end = i + 15
                    for j, t in enumerate(top_words):
                        if w == t:
                            continue
                        if t in words[start:end]:
                            A[keys_indices[w],j] += 1

            print("  Normalizing...")

            words_per_top = np.sum(A, axis=0)
            tops_per_word = np.sum(np.asarray(A > 0, 'i'), axis=1)
            rows, cols = A.shape
            for i in range(rows):
                for j in range(cols):
                    if words_per_top[j] == 0 or tops_per_word[i] == 0:
                        A[i,j] = 0
                    else:
                        A[i,j] = (A[i,j] / words_per_top[j]) * math.log(
                            float(cols) / tops_per_word[i])

            print("  SVD...")

            #U, S, Vt = scipy.sparse.linalg.svds(A, 100)
            s_A = scipy.sparse.csc_matrix(A)
            ut, s, vt = sparsesvd(s_A, 100)

            # <codecell>

            out = open(os.path.join(
                semantics_dir, "{0}-ut.bin".format(iso_639_3)), "wb")
            np.save(out, ut)
            out.close()

            out = open(os.path.join(
                semantics_dir, "{0}-s.bin".format(iso_639_3)), "wb")
            np.save(out, s)
            out.close()

            out = open(os.path.join(
                semantics_dir, "{0}-vt.bin".format(iso_639_3)), "wb")
            np.save(out, vt)
            out.close()

            with open(os.path.join(
                    semantics_dir, "{0}-indices.pickle".format(
                        iso_639_3)), "wb") as f:
                pickle.dump(keys_indices, f, 2)


if __name__ == "__main__":
    main(sys.argv)
