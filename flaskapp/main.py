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
from functions import getMainTerms, sortHeadlines
import string




def findTopics(date, 
               days_past=1, 
               dist_param=0.7, 
               link_method = 'single', 
               min_clust_size = 3, 
               max_n_topics = 10, 
               n_summ_words = 5):
    
    
    # get data from SQL table:
    host =  "/var/run/postgresql/"
    con = psycopg2.connect(database = 'nytimes', user = 'ubuntu', host=host)    
    sql_query = """
                SELECT * FROM alldata_lemm2 WHERE date_in>={} AND date_in<={};
                """.format(date-days_past, date)   
    DDtrunc = pd.read_sql_query(sql_query, con)
    DDtrunc = DDtrunc.ix[DDtrunc.content_lemmas != '',:]
    DDtrunc = DDtrunc.ix[DDtrunc.content_lemmas.apply(lambda x: x is not None),:]
    
    
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
    main_clusters = main_clusters[:max_n_topics]
    
    # gather lists of titles and contents for each cluster
    clustersizes = []
    main_titles = []
    main_urls = []
    main_articles_tfidf = []
    for c in main_clusters:
        clustersizes.append(c[1])
        art_inds = np.where(clusters == c[0])[0]
        art_inds = art_inds[sortHeadlines(DDtrunc, dist_matrix, art_inds)] # sort inds by relevance of headline
        titles = []
        urls = []
        vecs = []
        for ind in art_inds:
            if DDtrunc.title.iloc[ind] is not None:
                title = string.capitalize(DDtrunc.title.iloc[ind]) # capitalize 1st letters
                titles.append(title)
                urls.append(DDtrunc.url.iloc[ind])
                vecs.append(tfidf_model[dictionary.doc2bow(lemmas[ind])])
        main_titles.append(titles)
        main_urls.append(urls)
        main_articles_tfidf.append(vecs)
        

    # create key-word summary for each topic
    keywords = [getMainTerms(main_articles_tfidf[i], dictionary, n_summ_words) 
                    for i in range(len(main_articles_tfidf))]
    keywords = [s for s in keywords]
    
    

    return dict(titles = main_titles, 
                keywords = keywords,
                urls = main_urls,
                clustersizes = clustersizes)




