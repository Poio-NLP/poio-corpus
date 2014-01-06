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

    lines_to_delete_startswith = [
        u"// Chechen stemmer // released under GNU GPL 2.0 or later //"
    ]

    for line in f1:
        deleted_line = False
        for l in lines_to_delete_startswith:
            if line.startswith(l):
                f2.write("\n")
                deleted_line = True
        if deleted_line:
            continue

        # line = re_date.sub(re_empty, line)
        # line = re_dashes.sub("-", line)
        # line = re_arrows.sub("", line)
        # line = re_wrong_tags.sub("", line)

        # line = re_special1.sub("Le&lt;", line)
        # line = re_special2.sub("ci&lt;:", line)

        # line = re_img.sub(" ", line)

        f2.write(line)

    f1.close()
    f2.close()

if __name__ == "__main__":
    main(sys.argv)