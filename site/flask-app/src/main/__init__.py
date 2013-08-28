# -*- coding: utf-8 -*-
import os
import glob
import json
import pickle
import operator
import json

from flask import Flask, render_template, Markup, request, url_for, redirect, \
    flash, Response

import rdflib
import numpy as np
import scipy.spatial
import scipy.linalg
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import presage

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 8}

matplotlib.rc('font', **font)

from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

app = Flask(__name__)

languages_data = {}
languages_data_file = os.path.join(app.static_folder, 'langinfo',
    'languages_data.pickle')
with open(languages_data_file, "rb") as f:
    languages_data = pickle.load(f)


class DemoCallback(presage.PresageCallback):
    def __init__(self):
        presage.PresageCallback.__init__(self)
        self.buffer = ''

    def get_past_stream(self):
        return self.buffer
    
    def get_future_stream(self):
        return ''

# Presage owns callback, so we create it and disown it
callback = DemoCallback().__disown__()
prsg = presage.Presage(callback, os.path.join(app.static_folder, 'presage', 'bar.xml'))

###################################### Pages

@app.route("/")
def index_landing():
    #languages_data = get_languages_data()
    languages_json = json.dumps(languages_data)

    return render_template('index_landing.html',
        languages_json = Markup(languages_json))

@app.route("/_index")
def index():
    #languages_data = get_languages_data()
    languages_json = json.dumps(languages_data)

    return render_template('index.html',
        languages_json = Markup(languages_json))

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/corpus")
def corpus():
    #languages_data = get_languages_data()
    iso_codes = sorted(languages_data.keys())

    return render_template('corpus.html', languages_data = languages_data,
        languages = iso_codes)

@app.route("/tools")
def tools():
    #languages_data = get_languages_data()
    iso_codes = sorted(languages_data.keys())
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
        if not map_file:
            flash('No result for search term "{0}".'.format(term))
        else:
            return render_template('tools_semantics.html', iso=iso,
                map=map_file.encode('utf-8'), term=term)
    return render_template('tools_semantics.html', iso=iso,
                map=None, term=term)

@app.route("/tools/prediction/<iso>")
def tools_prediction(iso):
    return render_template('tools_prediction.html', iso=iso)

@app.route("/_presage")
def presage():
    string_buffer = request.args.get('text', '', type=str)
    callback.buffer = string_buffer
    prediction = list(prsg.predict())
    return Response(json.dumps(prediction), mimetype='application/json')

##################################### Helpers

def get_semantic_map(iso, term):
    plot_dir = os.path.join(app.static_folder, 'plots')
    plot_filename = u"{0}-{1}.png".format(iso, term)
    plot_filepath = os.path.join(plot_dir, plot_filename)
    if os.path.exists(plot_filepath):
        return plot_filename

    sem_dir = os.path.join(app.static_folder, 'semantics')

    indices_file = os.path.join(sem_dir, "{0}-indices.pickle".format(iso))
    with open(indices_file, "rb") as f:
        indices = pickle.load(f)
        keys = [k 
            for k, _ in sorted(indices.items(), key=operator.itemgetter(1))]
    if not term in indices:
        return None


    ut_file = os.path.join(sem_dir, "{0}-ut.bin".format(iso))
    with open(ut_file, "rb") as f:
        ut = np.load(f)
    s_file = os.path.join(sem_dir, "{0}-s.bin".format(iso))
    with open(s_file, "rb") as f:
        s = np.load(f)
    vt_file = os.path.join(sem_dir, "{0}-vt.bin".format(iso))
    with open(vt_file, "rb") as f:
        vt = np.load(f)

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

