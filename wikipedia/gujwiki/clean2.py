# -*- coding: utf-8 -*-
#
# Poio Corpus
#
# Copyright (C) 2009-2013 Poio Project
# Author: Eva Schinzel
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

# clean2-script for Gujarati language

# in order to run this script separately, enter in command line as follows:
# (while being located in directory "gujwiki") 
# c:\Python27\python.exe clean2.py gujwiki_cleaned1.xml gujwiki_cleaned2.xml

# in order to test this script, enter in python shell as follows:
# >>> import xml.etree.ElementTree as ET
# >>> ET.parse("gujwiki_cleaned2.xml")

import sys
import re
import codecs

if not len(sys.argv) == 3:
    print("In order to run this script, enter in command line as follows: clean2.py gujwiki_cleaned1.xml gujwiki_cleaned2.xml")
    sys.exit(1)

    
def main(argv):
    f1 = codecs.open(argv[1], "r", "utf-8")
    f2 = codecs.open(argv[2], "w", "utf-8")


    re_wrong_tags = re.compile(u"<ઓમ્ખ્પ્૨૬[^>]") 
    re_wrong_tags2 = re.compile(u"<સંદર્ભો[^>]") 
    re_wrong_tags3 = re.compile(u"<!-- આ લીટીની નીચે ફેરફાર કરવાની તમને છૂટ છે. --")
    re_inequation = re.compile("<\d")
    re_english = re.compile(u"The divisions between Asia and Europe[^<]*")



    for line in f1:
      
        line = re_wrong_tags.sub("", line)
        line = re_wrong_tags2.sub("", line)
        line = re_wrong_tags3.sub("", line)
        line = re_inequation.sub("", line)
        line = re_english.sub("\n", line)


        f2.write(line)

    f1.close()
    f2.close()

if __name__ == "__main__":
    main(sys.argv)
