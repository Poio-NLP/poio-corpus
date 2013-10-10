# -*- coding: utf-8 -*-
#
# Poio Corpus
#
# Copyright (C) 2009-2013 Poio Project
# Author: Eva Schinzel
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

# clean2-script for Sanskrit language

# in order to run this script separately, enter in command line as follows:
# (while being located in directory "sawiki") 
# c:\Python27\python.exe clean2.py sawiki_cleaned1.xml sawiki_cleaned2.xml

# in order to test this script, enter in python shell as follows:
# >>> import xml.etree.ElementTree as ET
# >>> ET.parse("sawiki_cleaned2.xml")

import sys
import re
import codecs

if not len(sys.argv) == 3:
    print("In order to run this script, enter in command line as follows: clean2.py sawiki_cleaned1.xml sawiki_cleaned2.xml")
    sys.exit(1)

def re_empty(matchobj):
    return ""

def main(argv):
    f1 = codecs.open(argv[1], "r", "utf-8")
    f2 = codecs.open(argv[2], "w", "utf-8")


    re_wrong_tags = re.compile("</noinclude[^>]")
    re_wrong_tags2 = re.compile(u"<कुल्याम्भोभिः[^>]")
    re_wrong_tags3 = re.compile(u"<एते[^>]")
    re_arrows = re.compile("<!-")
    re_arrow_in_brackets = re.compile("\(<\)")
    re_periodic_table = re.compile(u"एकं भौतिकतत्त्वम् अस्ति। Turma[^<]*") #list of elements of the periodic table
    re_genealogy = re.compile(u"मनु \| इला \| पुरुरवस् \| आयु \| नहुष \| ययाति \| पूरु \| जनमेजय[^<]*") #just a list of names
    re_english = re.compile(u"Valmiki \(Sanskrit: वाल्मीकि; Vālmīki\)is celebrated[^<]*") #article in english
    re_english2 = re.compile("Charles Francis Jenkins \(August 22, 1867[^<]*") #article in english
    re_meaningless_line = re.compile("mw\.loader\.using\('ext\.narayam\.rules\.sa[^<]*") #no meaningful content
    re_meaningless_line2 = re.compile(u"कोन्सेप्सिओन् \(IPA[^<]*") #no meaningful content
    re_meaningless_line3 = re.compile(u"वीथिका. चित्रम्:Rabbit 1hr old gnangarra[^<]*") #article containing only pictures of rabbits
    re_english3 = re.compile(u"नामाङ्किताः. This section refers to awards where Rahman[^<]*") #article in english



    for line in f1:

        line = re_arrows.sub("", line)
        line = re_arrow_in_brackets.sub("", line)
        line = re_periodic_table.sub("", line)
        line = re_genealogy.sub("", line)
        line = re_english.sub("", line)
        line = re_english2.sub("", line)
        line = re_english3.sub("", line)
        line = re_meaningless_line.sub("", line)
        line = re_meaningless_line2.sub("", line)
        line = re_meaningless_line3.sub("", line)
        line = re_wrong_tags.sub("", line)
        line = re_wrong_tags2.sub("", line)
        line = re_wrong_tags3.sub("", line)


        f2.write(line)

    f1.close()
    f2.close()

if __name__ == "__main__":
    main(sys.argv)