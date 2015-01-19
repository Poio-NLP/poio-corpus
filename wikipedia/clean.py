# -*- coding: utf-8 -*-
#
# Poio Corpus
#
# Copyright (C) 2009-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

import sys
#import regex as re
import re
import codecs
import html

re_apostroph = re.compile("\"")

def re_title_cleaned(matchobj):
    return matchobj.group(1) + re_apostroph.sub("", matchobj.group(2)) + matchobj.group(3)

def main(argv):
    f1 = codecs.open(argv[1], "r", "utf-8")
    f2 = codecs.open(argv[2], "w", "utf-8")

    f2.write("<xml>\n")

    re_title = re.compile("(title=\")(.*)(\">)")
    re_xml_tag = re.compile("<(?!/?doc)[^>]*>")
    re_and = re.compile("&")
    re_nbsp = re.compile("&nbsp;")
    re_lower = re.compile("(?<!^)<(?!/?doc|/?xml)")

    for i, line in enumerate(f1):
        line = html.unescape(line)

        line = re_title.sub(re_title_cleaned, line)

        line = re_xml_tag.sub(" ", line)
        line = re_and.sub("&amp;", line)
        line = re_lower.sub("&lt; ", line)
        line = re_nbsp.sub(" ", line)

        f2.write(line)

    f2.write("</xml>\n")

    f1.close()
    f2.close()

if __name__ == "__main__":
    main(sys.argv)
