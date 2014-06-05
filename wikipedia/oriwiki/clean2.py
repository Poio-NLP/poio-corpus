# -*- coding: utf-8 -*-
#
# Poio Corpus
#
# Copyright (C) 2009-2013 Poio Project
# Author: Eva Schinzel
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

# clean2-script for Oriya language

# in order to run this script separately, enter in command line as follows:
# (while being located in directory "orwiki") 
# c:\Python27\python.exe clean2.py orwiki_cleaned1.xml orwiki_cleaned2.xml

# in order to test this script, enter in python shell as follows:
# >>> import xml.etree.ElementTree as ET
# >>> ET.parse("orwiki_cleaned2.xml")

import sys
import re
import codecs

if not len(sys.argv) == 3:
    print("In order to run this script, enter in command line as follows: clean2.py orwiki_cleaned1.xml orwiki_cleaned2.xml")
    sys.exit(1)

    
def main(argv):
    f1 = codecs.open(argv[1], "r", "utf-8")
    f2 = codecs.open(argv[2], "w", "utf-8")

    re_wrong_tags = re.compile("<bookdata\.authors\.length") 
    re_wrong_tags2 = re.compile("var numforms = 0; var wikEdAutoUpdateUrl[^<]*") 
    re_wrong_tags3 = re.compile(u"<୧%")
    re_wrong_tags4 = re.compile("<!-- Please do not make edit tests here. Instead copy the following link, paste[^<]*") 
    re_dashes = re.compile(u"\-\-~~~~")
    re_code = re.compile(u"\<=2;i\+\+\) {  authorn.*")
    re_dashes2 = re.compile("\-\-")

    for line in f1:
        if line.startswith("<bookdata.authors.length "):
            f2.write("\n")
            continue

        if line.startswith("/*global mw, importScriptURI, importScript */"):
            f2.write("\n")
            continue

        if line.startswith("var numforms = 0; var wikEdAutoUpdateUrl; var citeUserDateFormat; var refTagURL;"):
            f2.write("\n")
            continue

        if line.startswith(u"<  ଏହି IRC (Internet Relay Chat) "):
            f2.write("\n")
            continue

        if line.startswith(u"<!-- ଯୁକ୍ତାକ୍ଷର ସବୁ "):
            f2.write("\n")
            continue

        if line.strip() == "<!--":
            f2.write("\n")
            continue

        line = re_wrong_tags.sub("", line)
        line = re_wrong_tags2.sub("", line)
        line = re_wrong_tags3.sub("", line)
        line = re_wrong_tags4.sub("", line)
        line = re_dashes.sub("", line)
        line = re_dashes2.sub("-", line)
        line = re_code.sub("", line)


        f2.write(line)

    f1.close()
    f2.close()

if __name__ == "__main__":
    main(sys.argv)
