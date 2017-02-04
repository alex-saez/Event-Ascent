#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 15:27:49 2017

@author: alex
"""

import spacy   

nlp = spacy.load('en')



#%%
doc = nlp(u"Apples and oranges are similar. Boots and hippos aren't.")
apples = doc[0]
oranges = doc[2]
boots = doc[6]
hippos = doc[8]

print(apples.vector.shape)

apples.similarity(oranges)
boots.similarity(hippos)

a = apples.vector + oranges.vector

#%%
import os
os.chdir('/Users/alex/Dropbox/Insight/Project/')
import get_data
D = get_data.getData()

t = D.content[0]
doc2 = nlp(t)

#%%
# GENSIM

from gensim import corpora, models, similarities, utils
#import pattern

# tokenize text
tokens = utils.tokenize("Hello, world! How is it hanging?", lower=True)
list(tokens) # to see tokens

# lemmatize text
utils.lemmatize("Hello, world! How is it hanging?")

# build dictionary from corpus of articles
docs = [D.content[i].split() for i in D.index]
dictionary = corpora.Dictionary(docs)

# save and load dictionary:
dictionary.save('nytdict.txtdic')
dictionary = corpora.Dictionary.load('nytdict.txtdic')

doc = "This is a Test"
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_bow

# corpora.dictionary methods:
dictionary.get(3021)
dictionary[3021] # same thing
[w for i,w in dictionary.items() if i==3021]
 
# now convert all articles in US section to BOW, this is called a Corpus
us_articles = [D.content[i].split() for i in D.index if D.section[i]=='us']
us_corpus = [dictionary.doc2bow(text) for text in us_articles]

# convert to tf-idf encoding:
from gensim import models
tfidf = models.TfidfModel(us_corpus)
tfidf[dictionary.doc2bow("This is a Test".lower().split())]

# train LSI model on corpus of US articles
lsi = models.LsiModel(us_corpus, id2word=dictionary, num_topics=20)  
index = similarities.MatrixSimilarity(lsi[us_corpus]) 

# compute similarity of 2 new docs, one in same corpus, one not
new_doc1 = list(D.content[D.section=='us'])[0]
new_doc2 = list(D.content[D.section=='travel'])[0]
vec_bow1 = dictionary.doc2bow(new_doc1.lower().split())
vec_lsi1 = lsi[vec_bow1] # convert the query to LSI space
sims1 = index[vec_lsi1] # perform a similarity query against the corpus
print(list(enumerate(sims1))) # print (document_number, document_similarity) 2-tuples 
sims1.mean() 
vec_bow2 = dictionary.doc2bow(new_doc2.lower().split())
vec_lsi2 = lsi[vec_bow2] # convert the query to LSI space
sims2 = index[vec_lsi2] # perform a similarity query against the corpus
sims2.mean() 


sims = sorted(enumerate(sims), key=lambda item: -item[1])

# LDA
lda = models.ldamodel.LdaModel(us_corpus, num_topics=10)
doc_lda = lda[doc_bow] # infer topic distribution in unseen doc
lda.update(other_corpus) # update existing doc

#%%
from gensim import corpora, models, similarities, utils

dictionary = corpora.Dictionary(L)
corpus = [dictionary.doc2bow(l) for l in L]
tfidf = models.tfidfmodel.TfidfModel(corpus)
tfidf[corpus[1]]

from gensim.matutils import jaccard, cossim
jaccard(L[1],L[2])

vec_bow1 = dictionary.doc2bow(L[1])
vec_bow2 = dictionary.doc2bow(L[2])
cossim(vec_bow1, vec_bow2)   

vec_tfidf1 = tfidf[corpus[1]]
vec_tfidf2 = tfidf[corpus[2]]
cossim(vec_tfidf1, vec_tfidf2)   

#%% Proper LDA 
import os
from gensim import corpora, models, similarities, utils
import pickle

os.chdir('/Users/alex/Dropbox/Insight/Project/')
DD = pickle.load(open('./D_lemm.obj','r'))
dictionary = corpora.Dictionary(DD.content_lemmas)
corpus = [dictionary.doc2bow(text) for text in DD.content_lemmas]
lda = models.ldamodel.LdaModel(corpus, num_topics=100)

vec_bow1 = dictionary.doc2bow(DD.content_lemmas[10])
lda[vec_bow1]



