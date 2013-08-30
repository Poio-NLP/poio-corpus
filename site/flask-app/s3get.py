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

os.system("{0} s3cmd.py get s3://poiocorpus {1} --acl-public --recursive --force --exclude=README.rst".format(
    sys.executable,
    os.path.join("src", "main", "static")))