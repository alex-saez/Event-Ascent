#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 18:04:19 2017

@author: alex
"""

from flaskapp import app
app.run(debug = True, port=8000)

#    import os
#
#    # Open a web browser pointing at the app.
#    port = 8000
#
#    os.system("open http://localhost:{0}/".format(port))
#
#    # Set up the development server on port 8000.
#    app.debug = True
#    app.run(port=port)
