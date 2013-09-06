# -*- coding: utf-8 -*-
#
# Poio Corpus
#
# Copyright (C) 2009-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

import sys
import regex as re
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

def main(argv):
    tree = ET.ElementTree(file=argv[1])
    root = tree.getroot()

    re_special_title = re.compile("\w+:\w", re.UNICODE)

    remove_list = list()

    for doc in root:
        title = doc.attrib['title']
        if re_special_title.match(title):
            remove_list.append(doc)
        elif len(doc.text) < 200:
            remove_list.append(doc)

    for doc in remove_list:
        root.remove(doc)
    tree.write(argv[2], encoding="UTF-8")

if __name__ == "__main__":
    main(sys.argv)
