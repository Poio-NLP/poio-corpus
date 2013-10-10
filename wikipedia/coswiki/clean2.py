# -*- coding: utf-8 -*-
#
# Poio Corpus
#
# Copyright (C) 2009-2013 Poio Project
# Author: Eva Schinzel
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

# clean2-script for Corsican language

# in order to run this script separately, enter in command line as follows: 
# (while being located in directory "cowiki")
# c:\Python27\python.exe clean2.py cowiki_cleaned1.xml cowiki_cleaned2.xml

# in order to test this script, enter in python shell as follows:
# >>> import xml.etree.ElementTree as ET
# >>> ET.parse("cowiki_cleaned2.xml")

import sys
import re
import codecs

if not len(sys.argv) == 3:
    print("In order to run this script, enter in command line as follows: clean2.py cowiki_cleaned1.xml cowiki_cleaned2.xml")
    sys.exit(1)

def re_empty(matchobj):
    return ""

def main(argv):
    f1 = codecs.open(argv[1], "r", "utf-8")
    f2 = codecs.open(argv[2], "w", "utf-8")

    lines_to_delete = [
        u"1669 Evenimenti. oooouığ*ğpü iüişppkoljukknhqwbjamqjnmwekqwqk2wlçg 124r565p6p6pootootootolyou yylel4ö3wö1qqqkwleekkrtkrfkkgvjfkgkjhgkhlçlhip0ppujkjhklykgthhjbnjnbngvmvmnsbchfjnfvchnvnhxyyyrhfkjjfrjhnfgfmnfnnfhfhnntgnjtjntgnngklhllhhlhllhlhldmzkmsodokrbçççgçgçgçşgşgşşgşglşgşlllblçblllhşhşşhşhnglglklkhllhlolhkkckxxjyqjhwjjakwjkkktrkjgkkgkkmkhkhkykkkkhkkıGHHHJK ILIKLIKFGSRDAWW<ıöhlbööböçhçhnçöççölhnököçkçjlkgljmgöhöhööhktuıuryıXEWOUIP ohlhlhllhlljlljlşhşllşpklpyooukuıudjzytwswuıuııııdoofor",
    ]

    for line in f1:
        if line.rstrip() in lines_to_delete:
            f2.write("\n")
            continue

        f2.write(line)

    f1.close()
    f2.close()

if __name__ == "__main__":
    main(sys.argv)