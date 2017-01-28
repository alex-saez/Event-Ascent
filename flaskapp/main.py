#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 09:50:26 2017

@author: alex
"""

import psycopg2
import pandas as pd
from gensim import corpora, models, similarities
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from functions import getMainTerms



def findTopics(date, 
               days_past=1, 
               dist_param=0.7, 
               link_method = 'single', 
               min_clust_size = 4, 
               n_summ_words = 5):
    
    
    # get data from SQL table:
    con = psycopg2.connect(database = 'nytimes', user = 'alex')    
    sql_query = """
                SELECT * FROM alldata_lemm WHERE date_in>={} AND date_in<={};
                """.format(date-days_past, date)   
    DDtrunc = pd.read_sql_query(sql_query, con)
    del DDtrunc['index']
    

    lemmas = list(DDtrunc.content_lemmas.apply(lambda x: x.split()))
    
    dictionary = corpora.Dictionary(lemmas)
    corpus = [dictionary.doc2bow(i) for i in lemmas]
    
    tfidf_model = models.TfidfModel(corpus)
    tfidfcorpus = tfidf_model[corpus]
    
    simil_matrix = similarities.MatrixSimilarity(tfidfcorpus)
    dist_matrix = 1 - cosine_similarity(simil_matrix)

    linkage_matrix = linkage(dist_matrix, method=link_method)
    clusters = fcluster(linkage_matrix, dist_param, criterion='distance')
    
    # find largest clusters:
    clust_sizes = np.bincount(clusters)
    main_clusters = [(i, clust_sizes[i]) for i in range(clust_sizes.size) 
                    if clust_sizes[i] >= min_clust_size]
    main_clusters = sorted(main_clusters, key=lambda x: x[1], reverse=True)
    
    # gather lists of titles and contents for each cluster
    main_titles = []
    main_articles_tfidf = []
    for c in main_clusters:
        art_inds = np.where(clusters == c[0])[0]
        titles = []
        vecs = []
        for ind in art_inds:
            titles.append(DDtrunc.title.iloc[ind])
            vecs.append(tfidf_model[dictionary.doc2bow(lemmas[ind])])
        main_titles.append(titles)
        main_articles_tfidf.append(vecs)
        

    # create key-word summary for each topic
    summaries = [getMainTerms(main_articles_tfidf[i], dictionary, n_summ_words) 
                    for i in range(len(main_articles_tfidf))]
    summaries = [s for s in summaries]

    return dict(titles = main_titles, summaries = summaries)


