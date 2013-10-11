# -*- coding: utf-8 -*-
import os
import glob
import json
import pickle
import operator
import json
import codecs
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from flask import Flask, render_template, Markup, request, url_for, redirect, \
    flash, Response
from flask.ext.mobility import Mobility
from flask.ext.mobility.decorators import mobile_template

#import rdflib
import numpy as np
import scipy.spatial
import scipy.linalg
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pressagio.callback
import pressagio

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 8}

matplotlib.rc('font', **font)

from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

app = Flask(__name__)
Mobility(app)

languages_data = {}
languages_data_file = os.path.join(app.static_folder, 'langinfo',
    'languages_data.pickle')
with open(languages_data_file, "rb") as f:
    languages_data = pickle.load(f)


class DemoCallback(pressagio.callback.Callback):
    def __init__(self, buffer):
        pressagio.callback.Callback.__init__(self)
        self.buffer = buffer

    def past_stream(self):
        return self.buffer
    
    def future_stream(self):
        return ''

###################################### Pages

@app.route("/")
@mobile_template('{mobile/}index.html')
def index(template):
    if request.MOBILE:
        languages_iso = {}
        for iso in languages_data:
            languages_iso[languages_data[iso]['label']] = iso
        languages = sorted(languages_iso.keys())
        return render_template(template, languages = languages,
            languages_iso = languages_iso)
        
    else:
        #languages_data = get_languages_data()
        languages_json = json.dumps(languages_data)

        return render_template(template,
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
    iso_codes_all = sorted(languages_data.keys())

    # filter iso codes for semantic maps
    iso_codes_semantics = []
    for iso in iso_codes_all:
        indices_file = os.path.join(app.static_folder, 'semantics',
            "{0}-indices.pickle".format(iso))
        if os.path.exists(indices_file):
            iso_codes_semantics.append(iso)

    # filter iso codes for text prediction
    iso_codes_prediction = []
    for iso in iso_codes_all:
        config_file = os.path.join(app.static_folder, 'prediction',
            "{0}.ini".format(iso))
        if os.path.exists(config_file):
            iso_codes_prediction.append(iso)

    return render_template('tools.html', languages_data = languages_data,
        languages_semantics = iso_codes_semantics,
        languages_prediction = iso_codes_prediction)

@app.route("/tools/semantics/<iso>", methods=["POST"])
def tools_semantics_term(iso):
    term = None
    if "term" in request.form:
        term = request.form["term"]
        term = "".join(
            [c for c in term if c.isalpha() or c.isdigit() or c==' '])\
            .rstrip().lower()
    target = url_for("tools_semantics", iso=iso, term=term)
    return redirect(target)

@app.route("/tools/semantics/<iso>")
@app.route("/tools/semantics/<iso>/<term>")
def tools_semantics(iso, term=None):
    #map_file = ""
    if term != None:
        graphdata = get_semantic_map(iso, term)
        # if not map_file:
        #     flash('No result for search term "{0}".'.format(term))
        # else:
        #     return render_template('tools_semantics.html', iso=iso,
        #         map=map_file.encode('utf-8'), term=term)
        graphdata_json = json.dumps(graphdata)
        return render_template('tools_semantics.html', iso=iso,
                map=None, term=term, graphdata_json = Markup(graphdata_json))
    return render_template('tools_semantics.html', iso=iso,
                map=None, term=term)

@app.route("/tools/prediction/<iso>")
def tools_prediction(iso):
    return render_template('tools_prediction.html', iso=iso)

@app.route("/_prediction")
def prediction():
    iso = request.args.get('iso', '', type=str)
    string_buffer = request.args.get('text', '').encode("utf-8")

    db_file = os.path.abspath(os.path.join(app.static_folder, 'prediction', "{0}.sqlite".format(iso)))
    config_file = os.path.join(app.static_folder, 'prediction', "{0}.ini".format(iso))
    config = configparser.ConfigParser()
    config.read(config_file)
    config.set("DefaultSmoothedNgramPredictor", "dbfilename", db_file)

    callback = DemoCallback(string_buffer)
    prsgio = pressagio.Pressagio(callback, config)
    predictions = prsgio.predict()

    return Response(json.dumps(predictions), mimetype='application/json')

@app.route("/documentation")
def documentation():
    return render_template('documentation.html')

@app.route("/imprint")
def imprint():
    return render_template('imprint.html')

@app.route("/privacy")
def privacy():
    return render_template('privacy.html')

@app.route("/licenses")
def licenses():
    return render_template('licenses.html')

##################################### Helpers

def get_semantic_map(iso, term):
    plot_dir = os.path.join(app.static_folder, 'plots')
    plot_filename = u"{0}-{1}.pickle".format(iso, term)
    plot_filepath = os.path.join(plot_dir, plot_filename)

    if os.path.exists(plot_filepath):
        inputfile = open(plot_filepath, 'rb')
        graphdata = pickle.load(inputfile)
        inputfile.close()
        return graphdata

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

    graphdata = []
    count = 0
    for element in tempU[:,1]:
        graphdata.append([words[count], element, tempU[:,2][count]])
        count += 1

    outputfile = open(plot_filepath, 'wb')
    pickle.dump(graphdata, outputfile)
    outputfile.close()
    return graphdata

    # graphdata_json = json.dumps(graphdata)
    # render_template('tools_semantics.html',
    #     graphdata_json = Markup(graphdata_json))

    # plt.clf()
    # plt.figure(1, figsize=(10,6))
    # plt.plot(tempU[:,1], tempU[:,2], marker="o", linestyle="None")
    # for label, x, y in zip(words, tempU[:,1], tempU[:,2]):
    #     plt.annotate(
    #         label, 
    #         xy = (x, y), xytext = (-5, 5),
    #         textcoords = 'offset points', ha = 'right', va = 'bottom',
    #         bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5))
    # #plt.show()
    # plt.savefig(plot_filepath)
    # return plot_filename