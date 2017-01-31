#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This file is part of the flask+d3 Hello World project.
"""
import json
from flask import Flask, request, render_template
import numpy as np
from main import findTopics



app = Flask(__name__)



@app.route("/")
def gindex():
    """
    When you request the gaus path, you'll get the gaus.html template.

    """
    mux = request.args.get('mux', '')
    muy = request.args.get('muy', '')
    if len(mux)==0: mux="3."
    if len(muy)==0: muy="3."
    return render_template("pagelayout4.html",mux=mux,muy=muy)



@app.route("/gdata")
@app.route("/gdata/<float:mux>/<float:muy>")
def gdata(ndata=10,mux=.5,muy=0.5):
    """
    On request, this returns a list of ``ndata`` randomly made data points.
    about the mean mux,muy

    :param ndata: (optional)
        The number of data points to return.

    :returns data:
        A JSON string of ``ndata`` data points.

    """

    #pull 'birth_month' from input field and store it
    #patient = int(request.args.get('mux'))
    
    # find topics
    topics = findTopics(5960)
    
    ntopics = len(topics['titles'])
    A = [len(i) for i in topics['titles']]
    x = np.arange(ntopics)
    y = [0]*ntopics
    #col = np.linspace(0,1,ntopics)[np.random.permutation(ntopics)]
    col = ["#156b87", "#876315", "#543510", "#872815"]*2
    t = ['topic{}'.format(i+1) for i in range(ntopics)]

#    summs_titles = []
#    for i,s in enumerate(topics['summaries']):
#        summs_titles.append(dict(summary = ' | '.join(s), titles = ''))
#        for t in topics['titles'][i]:
#             summs_titles.append(dict(summary = '', titles = t.decode('utf8').encode('ascii', 'ignore')))
#    
#    return render_template('output.html',topics=summs_titles)



    return json.dumps([{"_id": i, "x": x[i], "y": y[i], "area": A[i], "color": col[i], "tname": t[i]}
                        for i in range(ntopics)])
    
    

if __name__ == "__main__":
    import os

    port = 8000

    # Open a web browser pointing at the app.
    os.system("open http://localhost:{0}/".format(port))

    # Set up the development server on port 8000.
    app.run(port=port, debug = True)
