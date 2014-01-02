# -*- coding: utf-8 -*-
#
# Poio Corpus
#
# Copyright (C) 2009-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

import sys
import codecs
import re

def main(argv):
    if not len(argv) == 3:
        print("In order to run this script, enter in command line as follows: clean.py inputfile outpufile")
        sys.exit(1)

    f1 = codecs.open(argv[1], "r", "utf-8")
    f2 = codecs.open(argv[2], "w", "utf-8")

    for line in f1:
        line = re.sub("\[[^\[]*\]", "", line)
        f2.write(line)

    f1.close()
    f2.close()

if __name__ == "__main__":
    main(sys.argv)
