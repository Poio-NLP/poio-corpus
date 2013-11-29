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

    re_date = re.compile("\-?\-? ?\d\d?:\d\d, \d\d?. .{2,8}\.? \d\d\d\d \(CES?T\)")
    re_dashes = re.compile("\-\-")
    re_wrong_tags = re.compile("</noinclude[^>]")
    re_arrows = re.compile(u"Dia-  >==>==>==> Umgangs- >==>==>==> Standard- lekte &lt;==&lt;==&lt;==< sprachen &lt;==&lt;==&lt;==< varietäten ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ ┃ │        Niederdeutsch:      │                          ┃ ┃ │Westniederdt. ┆ Ostniederdt.│ Nord-                    ┃ ┃ │────────────────────────────│            Teu-          ┃ ┃ │        Mitteldeutsch:      │                          ┃ ┃ │Westmitteldt. ┆ Ostmittldt. │ Mittel-    to-           ┃ ┃ │───────┘Oberdeutsch:        │            nis-          ┃ ┃ │           Ost-/Südfränkisch│ Süd-                     ┃ ┃ │┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄│            men           ┃ ┃ │    ┊Schwäbisch┆            │ deutsch-                 ┃ ┃ │               ┆            │ land                     ┃ ┃ ═════Alemannisch╪════Bairisch══════════════════         ┃ ┃ │            ║  ┆                     │                 ┃ ┃  Schweiz     ║ Österreich                               ┃ ┃  Helvetismen ║ Austriazismen                            ┃ ┃                                                         ┃ ┃ ── ┄┄ Dialekträume: Forschungsgebiet Dialektologie      ┃ ┃ ══ Standardvarietäten: Forschungebiet Standardvarietäten┃ ")
    re_special1 = re.compile("Le<")
    re_special2 = re.compile("ci<:")
    re_img = re.compile(" [^ ]*\.jpg\|")

    lines_to_delete = [
        u"<!-- BITTE bei den Biografien der entsprechenden Personen auf der Bearbeitungsseite unten bei  Kategorien die folgende Zeile EINFÜGEN:",
        u"  </noinclude</includeonly»<includeonly</includeonly» BITTSCHÖN ENTFERN DII KOMMENTARE </includeonly</includeonly»",
        u"<!-- BITTE bei den Biografien der entsprechenden Personen auf der Bearbeitungsseite unten bei Kategorien die folgende Zeile EINFÜGEN:"
    ]

    for line in f1:
        if line.rstrip() in lines_to_delete:
            f2.write("\n")
            continue

        line = re_date.sub(re_empty, line)
        line = re_dashes.sub("-", line)
        line = re_arrows.sub("", line)
        line = re_wrong_tags.sub("", line)

        line = re_special1.sub("Le&lt;", line)
        line = re_special2.sub("ci&lt;:", line)

        line = re_img.sub(" ", line)

        f2.write(line)

    f1.close()
    f2.close()

if __name__ == "__main__":
    main(sys.argv)