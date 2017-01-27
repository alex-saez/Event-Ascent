#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 18:03:11 2017

@author: alex
"""

from flask import render_template, request
from flaskapp import app
from sqlalchemy import create_engine
import pandas as pd
import psycopg2
from main import findTopics

user = 'alex' #add your username here (same as previous postgreSQL)                      
host = 'localhost'
dbname = 'nytimes'
db = create_engine('postgres://%s%s/%s'%(user,host,dbname))
con = None
con = psycopg2.connect(database = dbname, user = user)


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



