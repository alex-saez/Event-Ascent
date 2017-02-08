#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 22:02:05 2017

@author: alex
"""
from gensim import utils
import pandas as pd
import numpy as np
import psycopg2
import datetime
from sqlalchemy import create_engine


def getData():   
    con = psycopg2.connect(database = 'nytimes', user = 'alex')
    sql_query = "SELECT * FROM alldata;"
    D = pd.read_sql_query(sql_query,con) # execute SQL query from Python
    del D['row.names']
    return D

def lemmatizeContent(D):  
    D['content_lemmas'] = D.content.apply(utils.lemmatize)
    D.content_lemmas =  D.content_lemmas.apply (lambda l: ' '.join(l))
    return D


def selectTimewin(D,t1,t2):
    ind = (D.date_in >= t1) & (D.date_in<=t2)
    return D.ix[ind,:]
    
def writeToSQL(D, name):
    engine = create_engine('postgres://%s@localhost/%s'%('alex','nytimes')) 
    D.to_sql(name, engine, if_exists='replace')


def selectSections(D):
    keep_sections = ['magazine',
                     'us',
                     'health',
                     'world',
                     'blogs',
                     'nytnow',
                     'science',
                     'upshot',
                     'opinion',
                     'arts',
                     't-magazine',
                     'technology',
                     'business',
                     'sports',
                     'obituaries',
                     'education',
                     'afternoonupdate',
                     'well']
    
    return D.iloc[[(D.loc[i,'section'] in keep_sections) for i in D.index],:]



def getMainTerms(tfidf_vec_list, dictionary, n_top_words=5):
    banned_words = ['mr','mrs','be']
    flat_list = [i for l in tfidf_vec_list for i in l]
    terms = [t[0] for t in flat_list]
    vals = [t[1] for t in flat_list]
    c = np.bincount(terms, weights=vals)
    term_counts = [(i, c[i]) for i in range(c.size)]
    term_counts = sorted(term_counts, key=lambda x: x[1], reverse=True)
    top_words = [dictionary.get(t[0])[:-3] for t in term_counts[:20]]
    top_words = [i for i in top_words if i not in banned_words]
    return top_words[:n_top_words]



def sortHeadlines(DDtrunc, dist_matrix, art_inds):
    # indices for sorting according to distance to others in the cluster
    DDtrunc_subset = DDtrunc.iloc[art_inds]
    mean_dists = np.sum(dist_matrix[art_inds,:][:,art_inds], axis=0)
    dist_ind = np.argsort(mean_dists)
    
    # indices for sorting according to section
    bad_sections = ['opinion','blogs','upshot','magazine','t-magazine']
    is_bad_section = [int(s in bad_sections) for s in DDtrunc_subset.section]      

    # indices for discriminating against wording punctuation that indicates less relevance
    has_bad_punct = []
    for t in DDtrunc_subset.title:
        if  t is not None:
            has_bad_punct.append(int(any([t.find(':')>-1, 
                                         t.find('?')>-1, 
                                         t.find('what you need to know')>-1, 
                                         t.find('what we know')>-1,
                                         t.find('the latest')>-1, 
                                         t.find('timeline-')>-1])))
        else:
            has_bad_punct.append(0)
    
    # finally sort first by section, then by wording, then by distance
    dtype = [('ind', int), ('sect', int), ('punct', int), ('dist', int)]
    values = [(i, is_bad_section[i], has_bad_punct[i], dist_ind[i]) for i in range(len(art_inds))]
    a = np.array(values, dtype=dtype) 
    a = np.sort(a, order=['sect', 'punct','dist'])
    return [k[0] for k in a]



def Date2Code(date):
    # input format: 'yyyy-mm-dd'   
    date_num = [int(i) for i in date.split('-')]
    day_diff = datetime.date(date_num[0],date_num[1],date_num[2]) - datetime.date(2016,3,15)
    return 5919 + day_diff.days

    
def Code2Date(datecode):
    diff = datetime.timedelta(days = datecode - 5919)
    date = datetime.date(2016,3,15) + diff
    day = str(date.day)
    month = str(date.month)
    year = str(date.year)
    if len(day)<2: day = '0'+day
    if len(month)<2: month = '0'+month
    return '{}-{}-{}'.format(year,month,day)
    
   
def assignColors(values, col1, col2):\
    # assigns hex color that linearly maps each value onto a color ramp between col1 and col2
    
    red1 = int(col1[1:3], 16)
    green1 = int(col1[3:5], 16)
    blue1 = int(col1[5:7], 16)
    red2 = int(col2[1:3], 16)
    green2 = int(col2[3:5], 16)
    blue2 = int(col2[5:7], 16)
     
    values = [i - min(values) for i in values]
    redramp = np.linspace(red1, red2, max(values)+1)
    greenramp = np.linspace(green1, green2, max(values)+1)
    blueramp = np.linspace(blue1, blue2, max(values)+1)
       
    return ['#%02x%02x%02x' % (redramp[values[i]], greenramp[values[i]], blueramp[values[i]])
            for i in range(len(values))]
    
    
    
    

#%%

#if __name__ == "__main__":
    
