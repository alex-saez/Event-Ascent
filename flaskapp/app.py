#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This file is part of the flask+d3 Hello World project.
"""
import json
from flask import Flask, request, render_template
from main import findTopics
from functions import Date2Code, assignColors



app = Flask(__name__)


@app.route("/")
@app.route('/<int:inputdate>')
def gindex():
    global data
   
    inputdate = request.args.get('inputdate','2016-04-25')
    
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
    
    
        
    return render_template("pagelayout6.html",
                           inputdate=inputdate, 
                           date_ok = date_ok,
                           data = data)



@app.route('/gdata/')
#@app.route('/gdata/<string:inputdate>')
def gdata(inputdate=None):    
    global data    
    return json.dumps(data)
   
#    inputdate_code = Date2Code(request.args.get('inputdate'))
#    
#        
#    # find topics
#    min_clust_size = 3
#    topics = findTopics(inputdate_code, min_clust_size=min_clust_size)
#    
#    # format data
#    ntopics = len(topics['titles'])
#    A = topics['clustersizes']
#    kw = [' | '.join(t) for t in topics['keywords']]
#    summ = ['<br />'.join(t) for t in topics['titles']]
#    headlines = topics['titles']
#
#    colscale = ["#e5e5e5","#e5d5cc","#e5c5b2","#e5b599","#e5a47f",
#                "#e59466","#e5844c","#e57433"]+["#e56419"]*1000
#    col = [colscale[i - min_clust_size] for i in A]
#   
#    return json.dumps([{"area": A[i], 
#                        "color": col[i], 
#                        "keywords": kw[i],
#                        "summary": summ[i],
#                        "headlines": headlines[i]} 
#                      for i in range(ntopics)])
#        

if __name__ == "__main__":
    import os

    # Open a web browser pointing at the app.
    port = 8000

    os.system("open http://localhost:{0}/".format(port))

    # Set up the development server on port 8000.
    app.debug = True
    app.run(port=port)