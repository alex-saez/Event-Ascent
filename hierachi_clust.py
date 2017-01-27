#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 13:30:26 2017

@author: alex
"""

from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import ward, complete, linkage, fcluster, fclusterdata, dendrogram
import numpy as np
from gensim import corpora, models, similarities, utils
import pickle
from gensim.matutils import cossim
from sklearn.metrics.pairwise import cosine_similarity


DD = pickle.load(open('/Users/alex/Dropbox/Insight/Project/D_lemm.obj', 'r'))
dictionary = corpora.Dictionary.load('/Users/alex/Dropbox/Insight/Project/nytdict.txtdic')

#%%
DDtrunc = DD.iloc[100:500,:]
d = list(DDtrunc.content_lemmas)

dictionary = corpora.Dictionary(d)
corpus = [dictionary.doc2bow(i) for i in d]

tfidf = models.TfidfModel(corpus)
tfidfcorpus = tfidf[corpus]
index = similarities.MatrixSimilarity(tfidfcorpus)
dist = 1 - cosine_similarity(index)

#vec_tfidf1 = tfidf[dictionary.doc2bow(d[4])]
#vec_tfidf2 = tfidf[dictionary.doc2bow(d[20])]
#sims = index[vec_tfidf1]
#cossim(vec_tfidf1, vec_tfidf2)


      
#%%
#linkage_matrix = linkage(dist, method='ward')
linkage_matrix = linkage(dist, method='single')

clusters = fcluster(linkage_matrix,.6, criterion='distance')
#clusters = fclusterdata(index, 10, criterion='distance', metric='seuclidean', method='single')
c = np.bincount(clusters)
clustcounts = [(i, c[i]) for i in range(c.size)]
clustcounts = sorted(clustcounts, key=lambda x: x[1], reverse=True)
#%%
a = np.where(clusters == 14)[0]
for i in range(a.size):
    print(DDtrunc.title.iloc[a[i]])

#%% dendrogram
fig, ax = plt.subplots(figsize=(15, 20)) # set size
ax = dendrogram(linkage_matrix, p=10, truncate_mode='lastp' ,orientation="right")

#plt.tick_params(\
#    axis= 'x',          # changes apply to the x-axis
#    which='both',      # both major and minor ticks are affected
#    bottom='off',      # ticks along the bottom edge are off
#    top='off',         # ticks along the top edge are off
#    labelbottom='off')

plt.tight_layout() #show plot with tight layout

#uncomment below to save figure
plt.savefig('newfig.png', dpi=200) #save figure as ward_clusters

#%% find most similar articles

tripletmat = [(i,j,dist[i,j]) for i in range(dist.shape[0]) for j in range(dist.shape[1])]
lowvals = [i for i in tripletmat if i[1]>i[0]]
lowvals = sorted(lowvals, key= lambda x: x[2])
lowvals[10:20]


# dist< 0.005 => same article
# dist< 0.03 => same topic

#%%
distvals = np.array([i[2] for i in lowvals])
plt.hist(distvals[distvals < 0.1],100)

def print_pair(dis, what='t'):
    global DDtrunc, lowvals, distvals
    ind1st = np.where(distvals > dis)[0][1]
    i,j = lowvals[ind1st][:2]
    if what=='t':
        print(DDtrunc.title.iloc[i])
        print('------------------------------------------------')
        print(DDtrunc.title.iloc[j])
    else:
        print(DDtrunc.content.iloc[i])
        print('------------------------------------------------')
        print(DDtrunc.content.iloc[j])


          