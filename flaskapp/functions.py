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

def getData():   
    con = psycopg2.connect(database = 'nytimes', user = 'alex')
    sql_query = "SELECT * FROM alldata;"
    return pd.read_sql_query(sql_query,con) ### execute SQL query from Python    

def prepareData(D):  
    D['content_lemmas'] = D.content.apply(utils.lemmatize)
    return D

def selectTimewin(D,t1,t2):
    ind = (D.date_in >= t1) & (D.date_in<=t2)
    return D.ix[ind,:]
    

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
    flat_list = [i for l in tfidf_vec_list for i in l]
    terms = [t[0] for t in flat_list]
    vals = [t[1] for t in flat_list]
    c = np.bincount(terms, weights=vals)
    term_counts = [(i, c[i]) for i in range(c.size)]
    term_counts = sorted(term_counts, key=lambda x: x[1], reverse=True)
    top_words = [dictionary.get(t[0])[:-3] for t in term_counts[:n_top_words]]
    return top_words
    
    


#%%

if __name__ == "__main__":
    L = prepareData(D)

    docs = [DD.content_lemmas[i] for i in DD.index]
    dictionary = corpora.Dictionary(docs)
    
    dictionary = corpora.Dictionary.load('/Users/alex/Dropbox/Insight/Project/nytdict.txtdic')
    
    from gensim.matutils import cossim
    vec_tfidf1 = tfidf[dictionary.doc2bow(DD.content_lemmas.iloc[1])]
    vec_tfidf2 = tfidf[dictionary.doc2bow(DD.content_lemmas.iloc[2])]
    cossim(vec_tfidf1, vec_tfidf2)   
    
    
    import pickle
    DD = prepareData(DD)
    pickle.dump(DD, open('D_lemm.obj', 'w')) # from package 'pickle', save any object to disk




