# -*- coding: utf-8 -*-
#
# Poio Corpus
#
# Copyright (C) 2009-2013 Poio Project
# Author: Eva Schinzel
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

# clean2-script for Malayalam language

# in order to run this script separately, enter in command line as follows:
# (while being located in directory "mlwiki") 
# c:\Python27\python.exe clean2.py mlwiki_cleaned1.xml mlwiki_cleaned2.xml

# in order to test this script, enter in python shell as follows:
# >>> import xml.etree.ElementTree as ET
# >>> ET.parse("mlwiki_cleaned2.xml")

import sys
import re
import codecs

if not len(sys.argv) == 3:
    print("In order to run this script, enter in command line as follows: clean2.py mlwiki_cleaned1.xml mlwiki_cleaned2.xml")
    sys.exit(1)

    
def main(argv):
    f1 = codecs.open(argv[1], "r", "utf-8")
    f2 = codecs.open(argv[2], "w", "utf-8")

    
    re_wrong_tags = re.compile("</noinclude[^>]") 
    re_wrong_tags2 = re.compile("<!-- Place INTERWIKI's ABOVE this line please") 
    re_wrong_tags3 = re.compile(u"<!---- The main postulates of Dalton's theory are[^<]*")
    re_wrong_tags4 = re.compile("<\.")
    re_wrong_tags5 = re.compile("<\r?\n")
    re_wrong_tags6 = re.compile("<!--\r?\n")
    re_wrong_tags7 = re.compile(u"<δആകുമ്പോഴെല്ലാം")
    re_inequation = re.compile(u"1<n\d<n")
    re_inequation2 = re.compile(u"\w<=\d")
    re_inequation3 = re.compile(u"pos <= n")
    re_ex = re.compile(u"ex:1 -- redirect 'Neap tide' goes to tide#Neap tide ex:2 -- two redirects go to the same section")


    for line in f1:
      
        line = re_wrong_tags.sub("", line)
        line = re_wrong_tags2.sub("", line)
        line = re_wrong_tags3.sub("", line)
        line = re_wrong_tags4.sub("", line)
        line = re_wrong_tags5.sub("\n", line)
        line = re_wrong_tags6.sub("\n", line)
        line = re_wrong_tags7.sub("", line)
        line = re_inequation.sub("", line)
        line = re_inequation2.sub("", line)
        line = re_inequation3.sub("", line)
        line = re_ex.sub("", line)


        f2.write(line)

    f1.close()
    f2.close()

if __name__ == "__main__":
    main(sys.argv)
