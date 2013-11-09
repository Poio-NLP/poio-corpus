# -*- coding: utf-8 -*-
#
# Poio Corpus
#
# Copyright (C) 2009-2013 Poio Project
# Author: Eva Schinzel
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

# clean2-script for Pali language

# in order to run this script separately, enter in command line as follows:
# (while being located in directory "pliwiki") 
# c:\Python27\python.exe clean2.py pliwiki_cleaned1.xml pliwiki_cleaned2.xml

# in order to test this script, enter in python shell as follows:
# >>> import xml.etree.ElementTree as ET
# >>> ET.parse("pliwiki_cleaned2.xml")

import sys
import re
import codecs

if not len(sys.argv) == 3:
    print("In order to run this script, enter in command line as follows: clean2.py pliwiki_cleaned1.xml pliwiki_cleaned2.xml")
    sys.exit(1)

    
def main(argv):
    f1 = codecs.open(argv[1], "r", "utf-8")
    f2 = codecs.open(argv[2], "w", "utf-8")


    re_wrong_tags = re.compile(u"<!--")
    re_inequation = re.compile(u"a\.getDate\(\)<10")




    for line in f1:
      
        line = re_wrong_tags.sub("", line)

        line = re_inequation.sub("", line)




        f2.write(line)

    f1.close()
    f2.close()

if __name__ == "__main__":
    main(sys.argv)
