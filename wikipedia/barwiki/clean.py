# -*- coding: utf-8 -*-

import regex as re
import codecs

f1 = codecs.open("barwiki.xml", "r", "utf-8")
f2 = codecs.open("barwiki-cleaned.xml", "w", "utf-8")

f2.write("<xml>\n")

re_xml_tag = re.compile("<(?!/?doc)[^>]*>")
re_and = re.compile("&")
re_title = re.compile("(title=\")(.*)(\">)")
re_apostroph = re.compile("\"")
re_lower = re.compile("< ")

re_date = re.compile("\-?\-? ?\d\d?:\d\d, \d\d?. .{2,8}\.? \d\d\d\d \(CES?T\)")
re_dashes = re.compile("\-\-")
re_wrong_tags = re.compile("</noinclude[^>]")
re_arrows = re.compile("(<==<==<==<|>==>==>==>)")
re_special1 = re.compile("Le<")
re_special2 = re.compile("ci<:")

def re_title_cleaned(matchobj):
    return matchobj.group(1) + re_apostroph.sub("", matchobj.group(2)) + matchobj.group(3)

def re_empty(matchobj):
    return ""

lines_to_delete = [
    9,
    6125,
    7319,
    14105,
    38477
]

for i, line in enumerate(f1):
    if i in lines_to_delete:
        f2.write("\n")
        continue

    line = re_title.sub(re_title_cleaned, line)

    line = re_xml_tag.sub(" ", line)
    line = re_and.sub("&amp;", line)
    line = re_lower.sub("&lt; ", line)

    line = re_date.sub(re_empty, line)
    line = re_dashes.sub("-", line)
    line = re_arrows.sub("", line)
    line = re_wrong_tags.sub("", line)

    line = re_special1.sub("Le&lt;", line)
    line = re_special2.sub("ci&lt;:", line)

    f2.write(line)

f2.write("</xml>\n")

f1.close()
f2.close()
