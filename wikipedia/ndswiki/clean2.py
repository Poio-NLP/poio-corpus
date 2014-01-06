# -*- coding: utf-8 -*-
#
# Poio Corpus
#
# Copyright (C) 2009-2013 Poio Project
# Author: Peter Bouda
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

import sys
import re    
import codecs

def main(argv):
    if not len(argv) == 3:
        print("In order to run this script, enter in command line as follows: clean2.py afrwiki_cleaned1.xml afrwiki_cleaned2.xml")
        sys.exit(1)

    f1 = codecs.open(argv[1], "r", "utf-8")
    f2 = codecs.open(argv[2], "w", "utf-8")

    lines_to_delete = [
    u'<-  Op disse Siet staht de Pressberichten, de de plattdüütsche Wikipedia över de Tiet rutgeven hett.'
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
