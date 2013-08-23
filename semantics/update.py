# -*- coding: utf-8 -*-
#
# Poio Corpus
#
# Copyright (C) 2009-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

import os
import glob
import re
import io
import math
import codecs
import zipfile
import shutil
from tempfile import mkdtemp

import requests
import numpy as np
import scipy.sparse
from sparsesvd import sparsesvd
import graf


semantics_dir = os.path.join("..", "build", "semantics")
os.chdir(semantics_dir)

corpus_dir = os.path.abspath(os.path.join("..", "corpus"))

for f in glob.glob(os.path.join(corpus_dir, "*.zip")):

	_, filename = os.path.split(os.path.abspath(f))
	filebasename, fileext = os.path.splitext(filename)
	language = filename[:3]

	print("Processing {0}".format(f))
	print("  File: {0}".format(filename))
	print("  Language: {0}".format(language))


	# From here on the code is a copy of the IPython notebook available at:
	# https://github.com/pbouda/notebooks/blob/master/Wikipedia.ipynb

	# <markdowncell>

	# ## Download stopwords and stop characters
	# 
	# A list of Bavarian stopwords was already compiled and is available for download. The next block of code download this list of stopwords and stores it in a variable `stopwords`. We will also download a list of characters that we want to ignore in Bavarian words and store it in the variable `ignorechars`:

	# <codecell>

	r = requests.get(
		"https://www.poio.eu/static/stopwords/{0}.txt".format(language),
		verify=False)
	stopwords = r.content.decode("utf-8").split()
	r = requests.get(
		"https://www.poio.eu/static/ignorechars/{0}.txt".format(language),
		verify=False)
	ignorechars = r.content.decode("utf-8")

	# <markdowncell>

	# ## Download, extract and parse the corpus
	# 
	# In the next step we will download and extract the corpus. The corpus is pre-compiled from Wikipedia dumps and was converted to a set of GrAF files. To parse the corpus we will use the library graf-python (see "Prerequisites" above). We will store each document of the Wikipedia as a Unicode string in the list `documents`:

	# <codecell>

	tmp_path = mkdtemp()

	z = zipfile.ZipFile(f)
	z.extractall(tmp_path)

	# <codecell>

	gp = graf.GraphParser()
	g = gp.parse(os.path.join(tmp_path, "{0}.hdr".format(filebasename)))

	text = codecs.open(os.path.join(
		tmp_path,"{0}.txt".format(filebasename)), "r", "utf-8")
	txt = text.read()
	text.close()

	documents = list()
	for n in g.nodes:
	    if n.id.startswith("doc..") and len(n.links) > 0 and len(n.links[0]) > 0:
	        doc = txt[n.links[0][0].start:n.links[0][0].end]
	        documents.append(doc)

	shutil.rmtree(tmp_path)

	# <markdowncell>

	# ## Build a dict for words and doc ids

	# <codecell>

	print("  Pre-processing...")

	re_ignore_chars = re.compile(u"[{0}]".format(ignorechars))
	def _words_for_document(doc):
	    words = doc.split()
	    words2 = list()

	    for w in words:
	        w = re_ignore_chars.sub("", w.lower())

	        if not w or w in stopwords:
	            continue
	        
	        words2.append(w)

	    return words2

	# <codecell>

	wdict = {}
	for i, d in enumerate(documents):
	    for w in _words_for_document(d):
	        if w in wdict:
	            wdict[w].append(i)
	        else:
	            wdict[w] = [i]

	# <markdowncell>

	# ## Pre-process

	# <codecell>

	# Which 1000 words occur most often?
	top_words = [k for k in sorted(wdict, key=lambda k: len(wdict[k]), reverse=True)][:1000]
	# get all words that appear at least 3 times and sort them
	keys = [k for k in wdict.keys() if len(wdict[k]) > 2]
	keys.sort()
	keys_indices = { w: i for i, w in enumerate(keys) }
	# create and empty count matrix
	A = np.zeros([len(keys), len(top_words)])

	# <markdowncell>

	# ## Process

	print("  Processing...")

	# <codecell>

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

	# <markdowncell>

	# ## Normalize

	# <codecell>

	print("  Normalizing...")

	words_per_top = np.sum(A, axis=0)
	tops_per_word = np.sum(np.asarray(A > 0, 'i'), axis=1)
	rows, cols = A.shape
	for i in range(rows):
	    for j in range(cols):
	        if words_per_top[j] == 0 or tops_per_word[i] == 0:
	            A[i,j] = 0
	        else:
	            A[i,j] = (A[i,j] / words_per_top[j]) * math.log(float(cols) / tops_per_word[i])


	# <markdowncell>

	# ## SVD calculation

	# <codecell>

	print("  SVD...")


	#U, S, Vt = scipy.sparse.linalg.svds(A, 100)
	s_A = scipy.sparse.csc_matrix(A)
	ut, s, vt = sparsesvd(s_A, 100)

	# <codecell>

	out = open("{0}-ut.bin".format(language), "wb")
	np.save(out, ut)
	out.close()

	out = open("{0}-s.bin".format(language), "wb")
	np.save(out, s)
	out.close()

	out = open("{0}-vt.bin".format(language), "wb")
	np.save(out, vt)
	out.close()

	# <codecell>

	import pickle
	with open("{0}-indices.pickle".format(language), "wb") as f:
	    pickle.dump(keys_indices, f, 2)

	# <codecell>

