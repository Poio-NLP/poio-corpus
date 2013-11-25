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

def re_title_cleaned(matchobj):
    return matchobj.group(1) + re_apostroph.sub("", matchobj.group(2)) + matchobj.group(3)

def re_empty(matchobj):
    return ""

def main(argv):
    f1 = codecs.open(argv[1], "r", "utf-8")
    f2 = codecs.open(argv[2], "w", "utf-8")


    lines_to_delete = [
    ]

    re_dashes = re.compile(r"----")
    re_dashes2 = re.compile(r"--")
    re_wrongtag = re.compile(r" <b")
    re_wrongtag2 = re.compile(r"<!-")

    for line in f1:
#        if line.rstrip() in lines_to_delete:
#            f2.write("\n")
#            continue

        if line.startswith("= GNU Free Documentation License = Version 1.2"):
            f2.write("\n")
            continue

        line = re_dashes.sub("", line)
        line = re_dashes2.sub("-", line)
        line = re_wrongtag.sub("", line)
        line = re_wrongtag2.sub("", line)

        f2.write(line)

    f1.close()
    f2.close()

if __name__ == "__main__":
    main(sys.argv)