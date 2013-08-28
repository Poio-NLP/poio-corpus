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

import poioapi.io.wikipedia_extractor
import poioapi.annotationgraph

def main(argv):

    parser = poioapi.io.wikipedia_extractor.Parser(argv[1])
    writer = poioapi.io.graf.Writer()

    converter = poioapi.io.graf.GrAFConverter(parser, writer)
    converter.parse()
    converter.write(argv[2])    

if __name__ == "__main__":
    main(sys.argv)
