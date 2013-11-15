# -*- coding: utf-8 -*-
#
# Poio Corpus
#
# Copyright (C) 2009-2013 Poio Project
# Author: Eva Schinzel
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

# clean2-script for Bengali language

# in order to run this script separately, enter in command line as follows:
# (while being located in directory "benwiki") 
# c:\Python27\python.exe clean2.py benwiki_cleaned1.xml benwiki_cleaned2.xml

# in order to test this script, enter in python shell as follows:
# >>> import xml.etree.ElementTree as ET
# >>> ET.parse("benwiki_cleaned2.xml")

import sys
import re
import codecs

if not len(sys.argv) == 3:
    print("In order to run this script, enter in command line as follows: clean2.py benwiki_cleaned1.xml benwiki_cleaned2.xml")
    sys.exit(1)

    
def main(argv):
    f1 = codecs.open(argv[1], "r", "utf-8")
    f2 = codecs.open(argv[2], "w", "utf-8")


    re_wrong_tags = re.compile(u"<\r?\n")
    re_wrong_tags2 = re.compile(u"<'")
    re_wrong_tags3 = re.compile(u"<!-- Note that there must be a space between the end of the redirect code and the template code for this to work properly")
    re_wrong_tags4 = re.compile(u"<১৫[^>]")
    re_wrong_tags5 = re.compile(u"<!--")
    re_inequation = re.compile(u"\w<\w+")
    re_inequation2 = re.compile(u"<=")
    re_inequation3 = re.compile(u"১<x<৫")
    re_inequation4 = re.compile(u"\(<কর'ল<করিল\), ধরত \(<ধর'ত<ধরিত\), বলে \(<ব'লে<বলিয়া\), হয়ে \(হ'য়ে<হইয়া\), দু জন \(<দু' জন\), চার শ \(<চার শ'\), চাল \(<চা'ল<চাউল\), আল \(<আ'ল<আইল\)")
    re_inequation5 = re.compile(u"\" < \"") #374777 zeichen 5480: komisches kleinerzeichen, das nicht weggehen will, da steht DAS: "r""k" < "r""k"−1.
    re_inequation6 = re.compile(u"\"k\" < \"r\"")



    for line in f1:
      
        line = re_wrong_tags.sub("\n", line)
        line = re_wrong_tags2.sub("", line)
        line = re_wrong_tags3.sub("", line)
        line = re_wrong_tags4.sub("", line)
        line = re_wrong_tags5.sub("", line)
        line = re_inequation.sub("", line)
        line = re_inequation2.sub("", line)
        line = re_inequation3.sub("", line)
        line = re_inequation4.sub("", line)
        line = re_inequation5.sub("", line)
        line = re_inequation6.sub("", line)




        f2.write(line)

    f1.close()
    f2.close()

if __name__ == "__main__":
    main(sys.argv)
