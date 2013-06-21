# -*- coding: utf-8 -*-

import sys
import regex as re
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
    re_arrows = re.compile("(<==<==<==<|>==>==>==>)")
    re_special1 = re.compile("Le<")
    re_special2 = re.compile("ci<:")


    lines_to_delete = [
    ]

    for line in f1:
        if line in lines_to_delete:
            f2.write("\n")
            continue

        line = re_date.sub(re_empty, line)
        line = re_dashes.sub("-", line)
        line = re_arrows.sub("", line)
        line = re_wrong_tags.sub("", line)

        line = re_special1.sub("Le&lt;", line)
        line = re_special2.sub("ci&lt;:", line)

        f2.write(line)

    f1.close()
    f2.close()

if __name__ == "__main__":
    main(sys.argv)