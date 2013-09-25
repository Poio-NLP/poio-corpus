# -*- coding: utf-8 -*-
#
# Poio Corpus
#
# Copyright (C) 2009-2013 Poio Project
# Author: Eva Schinzel
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

# tokenizer for languages in latin alphabet

# in order to run this script separately, enter in command line as follows:
# (the last argument - how many words you want to be displayed - is optional)
# c:\Python27\python.exe prepare.py XXwiki-DDDDDDDD.txt XXX.txt DDD...

# in this case: c:\Python27\python.exe prepare.py cowiki-20130907.txt stopwords.txt 2000

import codecs
import sys
import re
import collections

f1 = codecs.open(sys.argv[1], "r", "utf-8")
f2 = codecs.open(sys.argv[2], "w", "utf-8")

re_ignore_chars = re.compile(u"[`~!@#$%^&*()_\-–+=\\|\]}\[{'\";:/?.·•>,<†„“।॥\d]")



text = f1.read()
f1.close()
text = text.replace("\n", " ") 
text = re_ignore_chars.sub("", text)
words = text.split()


tokens = collections.defaultdict(int)  
for w in words:
    tokens[w] += 1

counter = 0        
for w in sorted(tokens, key=tokens.get, reverse=True):
    f2.write(w + " " + str(tokens[w]) + "\r\n")
    counter = counter + 1
    # if there is specified in command line, how many words
    # should be displayed in output file
    # (otherwise all words will be displayed)
    if len(sys.argv) == 4:
        if int(sys.argv[3]) == counter:
            break
     
f2.close()     
        