# -*- coding: utf-8 -*-
import os
import glob
import json

from flask import Flask, render_template, Markup
import rdflib

from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

app = Flask(__name__)

supported_languages =  [
    'bar',
    'ast',
    'arg',
    'nds',
    'gsw',
    'oci'
]

###################################### Pages

@app.route("/")
def index():
    languages_data = {}
    for iso in supported_languages:
        if not iso in languages_data:
            language_info = get_info_for_iso(iso)
            languages_data[iso] = language_info

    languages_json = json.dumps(languages_data)

    return render_template('index.html',
        languages_json = Markup(languages_json))

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/corpus")
def corpus():
    corpus_dir = os.path.join(app.static_folder, 'corpus')
    languages_data = {}
    for iso in supported_languages:
        corpus_files = []
        for f in glob.glob(os.path.join(corpus_dir, "{0}*.zip".format(iso))):
            corpus_files.append(os.path.basename(f))
        language_info = get_info_for_iso(iso)
        language_info['files'] = corpus_files
        languages_data[iso] = language_info

    iso_codes = sorted(supported_languages)
    return render_template('corpus.html',
        languages_data = languages_data,
        languages = iso_codes)


##################################### Helpers

def get_info_for_iso(iso):
    rv = cache.get(iso)
    if rv is None:
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
        cache.set(iso, rv)
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
