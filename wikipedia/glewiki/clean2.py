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

    re_xml = re.compile("<\?xml version=\"1.0\" ... \"")
    re_lt = re.compile("<\"")
    re_waste = re.compile(" <1%")
    re_url = re.compile("http://www.independent.ie/entertainment/news-gossip/graacute-moacuter-saying--i-do-as-gaeilge-1248240.html")
    re_dashes = re.compile("\-\-")

    lines_to_delete = [
        u"<!--",
        u"->    }}   <! -    To limit the number of changes on this page thank you to place    metadata (categories, interwiki) on this model in    sub-section of its documentation page, rather than here."
    ]

    for line in f1:
        if line.rstrip() in lines_to_delete:
            f2.write("\n")
            continue

        line = re_xml.sub("", line)
        line = re_lt.sub("\"", line)
        line = re_waste.sub("", line)
        line = re_url.sub("", line)
        line = re_dashes.sub("-", line)

        f2.write(line)

    f1.close()
    f2.close()

if __name__ == "__main__":
    main(sys.argv)