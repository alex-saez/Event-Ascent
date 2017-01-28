#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 18:03:11 2017

@author: alex
"""

from flask import Flask, render_template, request
#from flaskapp import app
import json
#import plotly
import numpy as np
from main import findTopics


app = Flask(__name__)




@app.route('/')
@app.route('/index')
def cesareans_page_fancy():
    
    topics = findTopics(date=5960)

    summs_titles = []
    for i,s in enumerate(topics['summaries']):
        summs_titles.append(dict(summary = ' | '.join(s), titles = ''))
        for t in topics['titles'][i]:
             summs_titles.append(dict(summary = '', titles = t.decode('utf8').encode('ascii', 'ignore')))
    
    return render_template('basic.html',topics=summs_titles)



@app.route('/input')
def topics_input():
    return render_template("input.html")

@app.route('/output')
def topics_output():
    #pull 'birth_month' from input field and store it
    patient = int(request.args.get('birth_month'))
    
    topics = findTopics(date=patient)

    summs_titles = []
    for i,s in enumerate(topics['summaries']):
        summs_titles.append(dict(summary = ' | '.join(s), titles = ''))
        for t in topics['titles'][i]:
             summs_titles.append(dict(summary = '', titles = t.decode('utf8').encode('ascii', 'ignore')))
    
    return render_template('output.html',topics=summs_titles)



#@app.route('/test')
#def index():
#    rng = pd.date_range('1/1/2011', periods=7500, freq='H')
#    ts = pd.Series(np.random.randn(len(rng)), index=rng)
#
#    graphs = [dict(
#                data=[
#                    dict(
#                    x=ts.index,  # Can use the pandas data structures directly
#                    y=ts
#                    )
#        ]
#        )
#    ]
#
#
#    # Add "ids" to each of the graphs to pass up to the client
#    # for templating
#    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]
#
#    # Convert the figures to JSON
#    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
#    # objects to their JSON equivalents
#    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
#
#    return render_template('index.html',
#                           ids=ids,
#                           graphJSON=graphJSON)

if __name__ == "__main__":
    app.run(debug=True)