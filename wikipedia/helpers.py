# -*- coding: utf-8 -*-
#
# Poio Corpus
#
# Copyright (C) 2009-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

import os
import sys


def wikipedia_extractor(file_path, wiki_name):
    os.system("{0} WikiExtractor.py -w -f tanl {1} {2}/extracted".format(
        sys.executable,
        file_path,
        wiki_name))
        
        


