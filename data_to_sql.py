#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 14:53:17 2017

@author: alex
"""

from sqlalchemy import create_engine
import pandas as pd

DD_sql = DD
DD_sql.content_lemmas =  DD_sql.content_lemmas.apply (lambda l: ' '.join(l))

engine = create_engine('postgres://%s@localhost/%s'%('alex','nytimes')) 

DD_sql.to_sql('alldata_lemm', engine, if_exists='replace')
