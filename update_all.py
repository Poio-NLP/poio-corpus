# -*- coding: utf-8 -*-
#
# Poio Corpus
#
# Copyright (C) 2009-2014 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

import os
import sys

arg_iso = ""
if len(sys.argv) > 1:
    arg_iso = sys.argv[1]

poio_path = os.path.dirname(os.path.realpath(__file__))

wikipedia_update = os.path.join(poio_path, "wikipedia", "update.py")
prediction_update = os.path.join(poio_path, "prediction", "update.py")
openadaptxt_update = os.path.join(poio_path, "openadaptxt", "update.py")
ngrams_update = os.path.join(poio_path, "ngrams", "update.py")

os.system("{0} {1} {2}".format(sys.executable, wikipedia_update, arg_iso))
os.system("{0} {1} {2}".format(sys.executable, prediction_update, arg_iso))
os.system("{0} {1} {2}".format(sys.executable, openadaptxt_update, arg_iso))
os.system("{0} {1} {2}".format(sys.executable, ngrams_update, arg_iso))
