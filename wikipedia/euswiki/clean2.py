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

    re_dashes = re.compile(r"--")
    re_wrongtag = re.compile(r"<- ")
    re_wrongtag2 = re.compile(r"</center")
    re_wrongtag3 = re.compile(u"<«ni»")
    re_wrongtag4 = re.compile(u"<1 ")
    re_wrongtag5 = re.compile(u"<!-(?=\r?\n)")
    re_wrongtag6 = re.compile(u"«<")
    re_lower = re.compile("(?<=\()<")
    re_lower2 = re.compile("(?<= )<(?=\*)")
    re_lower3 = re.compile("(?<=\")<(?=\")")
    re_lower4 = re.compile("(?<= )<(?=%)")
    re_lower6 = re.compile("(?<= )<(?=\))")
    re_lower8 = re.compile("(?<=3)<(?=a)")
    re_lower9 = re.compile("(?<=5)<(?=i)")

    lines_to_delete = [
    ]

    for line in f1:
#        if line.rstrip() in lines_to_delete:
#            f2.write("\n")
#            continue


        if line.startswith(u"Analisi matematikoan la Hölderren desberdintza, Otto Hölderek formulatua,"):
            f2.write("\n")
            continue

        line = re_dashes.sub("-", line)
        line = re_wrongtag.sub("", line)
        line = re_wrongtag2.sub("", line)
        line = re_wrongtag3.sub("", line)
        line = re_wrongtag4.sub("", line)
        line = re_wrongtag5.sub("", line)
        line = re_wrongtag6.sub("", line)
        line = re_lower.sub("&lt;", line)
        line = re_lower2.sub("&lt;", line)
        line = re_lower3.sub("&lt;", line)
        line = re_lower4.sub("&lt;", line)
        line = re_lower6.sub("&lt;", line)
        line = re_lower8.sub("&lt;", line)
        line = re_lower9.sub("&lt;", line)

        f2.write(line)

    f1.close()
    f2.close()

if __name__ == "__main__":
    main(sys.argv)