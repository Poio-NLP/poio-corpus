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
# (the last argument - how many words you want to be displayed - is optional (default: 1000)
# c:\Python27\python.exe prepare.py DDD...

# in this case: c:\Python27\python.exe prepare.py 4

import codecs
import os
import sys
import re
import shutil
import zipfile
import collections
import glob
from tempfile import mkdtemp
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

    
#defining length of stopword list (default: 1000)
if len(sys.argv) == 1:
    length_stopwordlist = 1000
elif len(sys.argv) == 2:
    length_stopwordlist = int(sys.argv[1])
else:
    print("1 or 2 arguments required")
    sys.exit(1)

    
config_file = os.path.join('..', 'config.ini')
config = configparser.ConfigParser()
config.read(config_file)

corpus_dir = os.path.join("..", "build", "corpus")
print(corpus_dir) #p0
for iso_639_3 in config.options("LanguagesISOMap"):
    print(iso_639_3) #print1
    for f in glob.glob(
        os.path.join(corpus_dir, "{0}wiki*.zip".format(
            iso_639_3))):
        
        print(f) #....
        
        _, filename = os.path.split(os.path.abspath(f))
        filebasename, _ = os.path.splitext(filename)
        print(filebasename) #p...
        try:
            tmp_path = mkdtemp()

            z = zipfile.ZipFile(f)
            z.extractall(tmp_path)  

            text_files = glob.glob(os.path.join(
                tmp_path,"{0}*.txt".format(filebasename)))
            f1 = codecs.open(text_files[0], "r", "utf-8")
            text = f1.read()
            f1.close()            
            
            print(text[:1000])
            
        finally:
            try:
                shutil.rmtree(tmp_path)
            except WindowsError:
                pass   

                
        stopwords_file = os.path.join("..", "build", "stopwords",
            "{0}.txt".format(iso_639_3))
        f2 = codecs.open(stopwords_file, "w", "utf-8")

        separators_file = os.path.join("..", "build", "separators", "allchars.txt")
        s_f = codecs.open(separators_file, "r", "utf-8")
        separators = s_f.read()
        s_f.close()
        re_ignore_chars = re.compile(u"[{0}]".format(separators))


        text = text.replace("\n", " ") 
        text = re_ignore_chars.sub("", text)
        words = text.split()


        tokens = collections.defaultdict(int)  
        for w in words:
            tokens[w] += 1
       
        for w in sorted(tokens, key=tokens.get, reverse=True)[:length_stopwordlist]:
            f2.write(w + " " + str(tokens[w]) + "\r\n")
    
        f2.close()     
