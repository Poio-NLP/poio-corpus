# -*- coding: utf-8 -*-
#
# Poio Corpus
#
# Copyright (C) 2009-2013 Poio Project
# Author: Eva Schinzel
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

# clean2-script for Sinhala language

# in order to run this script separately, enter in command line as follows:
# (while being located in directory "sinwiki") 
# c:\Python27\python.exe clean2.py sinwiki_cleaned1.xml sinwiki_cleaned2.xml

# in order to test this script, enter in python shell as follows:
# >>> import xml.etree.ElementTree as ET
# >>> ET.parse("sinwiki_cleaned2.xml")

import sys
import re
import codecs

if not len(sys.argv) == 3:
    print("In order to run this script, enter in command line as follows: clean2.py sinwiki_cleaned1.xml sinwiki_cleaned2.xml")
    sys.exit(1)

    
def main(argv):
    f1 = codecs.open(argv[1], "r", "utf-8")
    f2 = codecs.open(argv[2], "w", "utf-8")


    re_wrong_tags = re.compile(u"<!--ගණිතය") 
    re_wrong_tags2 = re.compile("<\d") 
    re_wrong_tags3 = re.compile(u"<සිංගුර්<සිංග්පුර්<සිංහපූර්")
    re_wrong_tags4 = re.compile("<=")
    re_wrong_tags5 = re.compile("<r=1")
    re_wrong_tags6 = re.compile("</gallery[^>]")
    re_wrong_tags7 = re.compile("<uybridge")
    re_wrong_tags8 = re.compile("</ref[^>]")
    re_wrong_tags9 = re.compile("<GTX")
    re_inequation = re.compile(u"Δ\w < 0")
    re_inequation2 = re.compile(u"<funcs\.length")
    re_inequation3 = re.compile(u"<prodtypes\.length")



    for line in f1:
      
        line = re_wrong_tags.sub("", line)
        line = re_wrong_tags2.sub("", line)
        line = re_wrong_tags3.sub("", line)
        line = re_wrong_tags4.sub("", line)
        line = re_wrong_tags5.sub("", line)
        line = re_wrong_tags6.sub("", line)
        line = re_wrong_tags7.sub("", line)
        line = re_wrong_tags8.sub("", line)
        line =re_wrong_tags9.sub("", line)
        line = re_inequation.sub("", line)
        line = re_inequation2.sub("", line)
        line = re_inequation3.sub("", line)


        f2.write(line)

    f1.close()
    f2.close()

if __name__ == "__main__":
    main(sys.argv)
