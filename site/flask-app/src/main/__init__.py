# -*- coding: utf-8 -*-
import os
import glob
import json
import pickle
import operator

from flask import Flask, render_template, Markup, request, url_for, redirect
import rdflib
import numpy as np
import scipy.spatial
import scipy.linalg
import matplotlib.pyplot as plt
import matplotlib

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 8}

matplotlib.rc('font', **font)

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
def index_landing():
    languages_data = get_languages_data()
    languages_json = json.dumps(languages_data)

    return render_template('index_landing.html',
        languages_json = Markup(languages_json))

@app.route("/_index")
def index():
    languages_data = get_languages_data()
    languages_json = json.dumps(languages_data)

    return render_template('index.html',
        languages_json = Markup(languages_json))

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/corpus")
def corpus():
    languages_data = get_languages_data()
    iso_codes = sorted(supported_languages)

    return render_template('corpus.html', languages_data = languages_data,
        languages = iso_codes)

@app.route("/tools")
def tools():
    languages_data = get_languages_data()
    iso_codes = sorted(supported_languages)
    return render_template('tools.html', languages_data = languages_data,
        languages = iso_codes)

@app.route("/tools/semantics/<iso>", methods=["POST"])
def tools_semantics_term(iso):
    term = None
    if "term" in request.form:
        term = request.form["term"].decode('utf-8')
        term = "".join(
            [c for c in term if c.isalpha() or c.isdigit() or c==' '])\
            .rstrip().lower()
    target = url_for("tools_semantics", iso=iso, term=term)
    return redirect(target)

@app.route("/tools/semantics/<iso>")
@app.route("/tools/semantics/<iso>/<term>")
def tools_semantics(iso, term=None):
    map_file = ""
    if term != None:
        map_file = get_semantic_map(iso, term)
    return render_template('tools_semantics.html', iso=iso,
        map=map_file.encode('utf-8'), term=term)


##################################### Helpers

def get_languages_data():
    corpus_dir = os.path.join(app.static_folder, 'corpus')
    languages_data = {}
    for iso in supported_languages:
        corpus_files = []
        for f in glob.glob(os.path.join(corpus_dir, "{0}*.zip".format(iso))):
            corpus_files.append(os.path.basename(f))
        language_info = get_info_for_iso(iso)
        language_info['files'] = corpus_files
        languages_data[iso] = language_info
    return languages_data    

def get_semantic_map(iso, term):
    plot_dir = os.path.join(app.static_folder, 'plots')
    plot_filename = u"{0}-{1}.png".format(iso, term)
    plot_filepath = os.path.join(plot_dir, plot_filename)
    if os.path.exists(plot_filepath):
        return plot_filename

    sem_dir = os.path.join(app.static_folder, 'semantics')

    ut_file = os.path.join(sem_dir, "{0}-ut.bin".format(iso))
    with open(ut_file, "rb") as f:
        ut = np.load(f)
    s_file = os.path.join(sem_dir, "{0}-s.bin".format(iso))
    with open(s_file, "rb") as f:
        s = np.load(f)
    vt_file = os.path.join(sem_dir, "{0}-vt.bin".format(iso))
    with open(vt_file, "rb") as f:
        vt = np.load(f)
    indices_file = os.path.join(sem_dir, "{0}-indices.pickle".format(iso))
    with open(indices_file, "rb") as f:
        indices = pickle.load(f)
        keys = [k 
            for k, _ in sorted(indices.items(), key=operator.itemgetter(1))]

    reconstructed_matrix = np.dot(ut.T, np.dot(np.diag(s), vt))
    tree = scipy.spatial.cKDTree(reconstructed_matrix)
    neighbours = tree.query(reconstructed_matrix[indices[term]], k=50)
    subset = reconstructed_matrix[neighbours[1]]
    words = [keys[i] for i in neighbours[1]]
    tempU, tempS, tempVt = scipy.linalg.svd(subset)

    coords = tempU[:,1:3]
    plt.clf()
    plt.figure(1, figsize=(10,6))
    plt.plot(tempU[:,1], tempU[:,2], marker="o", linestyle="None")
    for label, x, y in zip(words, tempU[:,1], tempU[:,2]):
        plt.annotate(
            label, 
            xy = (x, y), xytext = (-5, 5),
            textcoords = 'offset points', ha = 'right', va = 'bottom',
            bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5))
    #plt.show()
    plt.savefig(plot_filepath)
    return plot_filename

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
