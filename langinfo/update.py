# -*- coding: utf-8 -*-
#
# Poio Corpus
#
# Copyright (C) 2009-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE.TXT

import sys
import os
import glob
import pickle

from config import Config
import rdflib

###################################### Main

def main(argv):
    config_file = file(os.path.join('..', 'config.ini'))
    config = Config(config_file)

    languages_data = {}
    for lang in config['supported_languages']:
        iso = lang['iso_639_3']
        language_info = get_language_info(iso)
        languages_data[iso] = language_info

    langinfo_dir = os.path.join("..", "build", "langinfo")
    pickle_file = os.path.join(langinfo_dir, "languages_data.pickle")
    with open(pickle_file, "wb") as f:
        pickle.dump(languages_data, f)

###################################### Helpers

def get_language_info(iso):
    corpus_dir = os.path.abspath(os.path.join("..", "build", "corpus"))
    corpus_files = []
    for f in glob.glob(os.path.join(corpus_dir, "{0}*.zip".format(iso))):
        corpus_files.append(os.path.basename(f))
    language_info = get_info_for_iso(iso)
    language_info['files'] = corpus_files
    return language_info

def get_info_for_iso(iso):
    rdf = RdfIso(iso)
    (latitude, longitude) = rdf.geo()
    label = rdf.label()
    rv = {
        'label' : label,
        'geo': {
            'lat': latitude,
            'lon': longitude
        }
    }
    return rv

class RdfIso:

    def __init__(self, iso):
        self.g = rdflib.Graph()
        result = self.g.parse(
            "http://glottolog.org/resource/languoid/iso/{0}.rdf".format(iso))
        self.subject = self.g.subjects().next()

    def geo(self):
        latitude = self.g.value(
            self.subject,
            rdflib.term.URIRef(
                u"http://www.w3.org/2003/01/geo/wgs84_pos#lat"))

        longitude = self.g.value(
            self.subject,
            rdflib.term.URIRef(
                u"http://www.w3.org/2003/01/geo/wgs84_pos#long"))

        return (latitude.toPython(), longitude.toPython())

    def label(self):
        name = self.g.value(
            self.subject,
            rdflib.term.URIRef(
                u"http://www.w3.org/2004/02/skos/core#prefLabel"))
        return name.toPython()

if __name__ == "__main__":
    main(sys.argv)
