# -*- coding: utf-8 -*-
#
# Poio Corpus
#
# Copyright (C) 2009-2013 Poio Project
# Author: Eva Schinzel
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

# clean2-script for Telugu language

# in order to run this script separately, enter in command line as follows:
# (while being located in directory "telwiki") 
# c:\Python27\python.exe clean2.py telwiki_cleaned1.xml telwiki_cleaned2.xml

# in order to test this script, enter in python shell as follows:
# >>> import xml.etree.ElementTree as ET
# >>> ET.parse("telwiki_cleaned2.xml")

import sys
import re
import codecs

if not len(sys.argv) == 3:
    print("In order to run this script, enter in command line as follows: clean2.py telwiki_cleaned1.xml telwiki_cleaned2.xml")
    sys.exit(1)

def re_empty(matchobj):
    return ""
    
def main(argv):
    f1 = codecs.open(argv[1], "r", "utf-8")
    f2 = codecs.open(argv[2], "w", "utf-8")


    re_wrong_tags = re.compile(u"<!--;ట్విట్టర్ తరహా నివేదిక") 
    re_wrong_tags2 = re.compile(u"<ల\.") 
    re_wrong_tags3 = re.compile(u"</open")
    re_wrong_tags4 = re.compile(u"<\*కేయు")
    re_wrong_tags5 = re.compile(u"<=")
    re_wrong_tags6 = re.compile("</noinclude[^>]")
    re_wrong_tags7 = re.compile(u"<references/")
    re_nul = re.compile(chr(0))
       

    for line in f1:
      
        line = re_wrong_tags.sub("", line)
        line = re_wrong_tags2.sub("", line)
        line = re_wrong_tags3.sub("", line)
        line = re_wrong_tags4.sub("", line)
        line = re_wrong_tags5.sub("", line)
        line = re_wrong_tags6.sub("", line)
        line = re_wrong_tags7.sub("", line)
        line = re_nul.sub("", line) 


        f2.write(line)

    f1.close()
    f2.close()

if __name__ == "__main__":
    main(sys.argv)
