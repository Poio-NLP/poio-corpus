# -*- coding: utf-8 -*-
#
# Poio Corpus
#
# Copyright (C) 2009-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

import sys
import re
import codecs

def main(argv):
    f1 = codecs.open(argv[1], "r", "utf-8")
    f2 = codecs.open(argv[2], "w", "utf-8")

    re_lt = re.compile(u"\(<něm")
    re_waste = re.compile(u" …--<")

    lines_to_delete = [
        u" </noinclude</includeonly»"
    ]

    for line in f1:
        if line.rstrip() in lines_to_delete:
            f2.write("\n")
            continue
    
        line = re_lt.sub(u"(&lt;něm", line)
        line = re_waste.sub("", line)

        f2.write(line)

    f1.close()
    f2.close()

if __name__ == "__main__":
    main(sys.argv)