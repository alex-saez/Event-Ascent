#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 09:50:26 2017

@author: alex
"""
import json
from flask import request, render_template
from flaskapp import app
from main import findTopics
from functions import Date2Code, assignColors



@app.route("/")
@app.route('/<int:inputdate>')
def gindex():
    global data
   
    inputdate = request.args.get('inputdate','04/25/2016')
    
    # check date is within range
    inputdate_code = Date2Code(inputdate)
    if (inputdate_code > 6246) | (inputdate_code < 5919):        
        date_ok = 0
        data = []
        
    else:
        date_ok = 1

        # find topics
        topics = findTopics(inputdate_code)    
        
        # format data
        ntopics = len(topics['titles'])
        A = topics['clustersizes']
        kw = [' | '.join(t) for t in topics['keywords']]
        summ = ['<br />'.join(t) for t in topics['titles']]
        headlines = topics['titles']
        urls = topics['urls']
        col = assignColors(A, "#f2f0f7", "#807dba")
        data = [{"area": A[i], 
                "color": col[i], 
                "keywords": kw[i],
                "summary": summ[i],
                "headlines": headlines[i],
                "urls": urls[i]} 
              for i in range(ntopics)]
    
    
        
    return render_template("mainpage.html",
                           inputdate=inputdate, 
                           date_ok = date_ok,
                           data = data)


@app.route('/gdata/')
#@app.route('/gdata/<string:inputdate>')
def gdata(inputdate=None):    
    global data    
    return json.dumps(data)

   
@app.route('/about/')
#@app.route('/gdata/<string:inputdate>')
def display_about():    
    return render_template("aboutpage.html")

   
@app.route('/slideshow/')
#@app.route('/gdata/<string:inputdate>')
def display_slides():    
    return render_template("slidespage.html")
   
