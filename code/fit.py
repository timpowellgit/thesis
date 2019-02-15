from __future__ import print_function

import os
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS
import numpy as np
import re
import math
import pickle
import operator
from sklearn.linear_model import RandomizedLogisticRegression

import tempfile
from sklearn.externals.joblib import Memory

edgelist,onesandzeros, cases, files, filenames =pickle.load(open('preprocessed.pickle', 'rb'))
vectorizer = CountVectorizer(binary = True, input = 'filename', min_df=2, stop_words =ENGLISH_STOP_WORDS)
vocab = vectorizer.fit_transform(files)
print('vectorized')
vocabtoarray = vocab.toarray()
usezero = np.zeros_like(vocabtoarray[0])
Xintersection = []
intersection = np.zeros_like(vocab.toarray())
for i,pair in enumerate(onesandzeros):
    print(i,' of ', len(onesandzeros))
    usezero2 = usezero.copy()
    #print(i, 'zeros loaded, to index now')
    indexa = filenames.index(pair[0])
    indexb = filenames.index(pair[1])
    #print('indexed gonna do the intersection now')
    indices= list(set(np.nonzero(vocabtoarray[indexa])[0]).intersection(np.nonzero(vocabtoarray[indexb])[0]))
    #print('intersection found, gonna put the 1s at indices')
    intersects = np.put(usezero2,indices,1)
    Xintersection.append(usezero2)
    #print('indices put, and appended')
print(len(Xintersection))

cachedir = tempfile.mkdtemp()
mem = Memory(cachedir=cachedir, verbose=1)

selector = RandomizedLogisticRegression(n_resampling=300,random_state=101, memory =mem)
ys = [1 if (i+1)*2 <= len(onesandzeros) else 0 for i,x in enumerate(onesandzeros)]
print(len(Xintersection[0]), len(Xintersection))
selector.fit(Xintersection,ys)
print(sum(selector.get_support() !=0))
print(len(selector.all_scores_))
print(len(vectorizer.vocabulary_))
with open('xsandys', 'wb') as handle:
  pickle.dump(Xintersection, handle)
  pickle.dump(ys, handle)
higherscores = []
for i,x in enumerate(selector.all_scores_):
    if x != 0:

        term = vectorizer.vocabulary_.keys()[vectorizer.vocabulary_.values().index(i)]
        termandscore = [x[0],term]

        higherscores.append(termandscore)
print('higherscores length', len(higherscores))
scorefile = open('scorefile.txt', 'w')
for y in sorted(higherscores,key=operator.itemgetter(0), reverse=True):
    scorefile.write('%s\n' %(str(y)))

# edgelist,onesandzeros, cases, files, filenames =pickle.load(open('preprocessed.pickle', 'rb'))
# vectorizer = CountVectorizer(binary = True, input = 'filename', stop_words= ENGLISH_STOP_WORDS)
# vocab = vectorizer.fit_transform(files)
# print(vectorizer.stop_words_)
# print('vectorized')
# vocabtoarray = vocab.toarray()
# print('len vocab',len(vocabtoarray[0]))
# usezero = np.zeros_like(vocabtoarray[0])
# print('len usezero',len(usezero))

# Xintersection = []
# intersection = np.zeros_like(vocab.toarray())
# for i,pair in enumerate(onesandzeros):
#     print(i,' of ', len(onesandzeros))
#     usezero2 = usezero.copy()
#     #print(i, 'zeros loaded, to index now')
#     indexa = filenames.index(pair[0])
#     indexb = filenames.index(pair[1])
#     #print('indexed gonna do the intersection now')
#     indices= list(set(np.nonzero(vocabtoarray[indexa])[0]).intersection(np.nonzero(vocabtoarray[indexb])[0]))
#     #print('intersection found, gonna put the 1s at indices')
#     intersects = np.put(usezero2,indices,1)
#     print('len usezero in loop',len(usezero2))

#     Xintersection.append(usezero2)
#     #print('indices put, and appended')
# print(len(Xintersection))

# cachedir = tempfile.mkdtemp()
# mem = Memory(cachedir=cachedir, verbose=1)

# selector = RandomizedLogisticRegression(n_resampling=300,random_state=101,memory =mem)
# ys = [1 if (i+1)*2 <= len(onesandzeros) else 0 for i,x in enumerate(onesandzeros)]
# print(len(Xintersection[0]), len(Xintersection))
# selector.fit(Xintersection,ys)
# print('number scores that arent zero ',sum(selector.get_support() !=0))
# print(len(selector.all_scores_))
# print(len(vectorizer.vocabulary_))
# with open('../data/Xs_Ys.pickle', 'wb') as handle:
#   pickle.dump(Xintersection, handle)
#   pickle.dump(ys, handle)
# higherscores = []
# for i,x in enumerate(selector.all_scores_):
#     if x != 0:
#         term = vectorizer.vocabulary_.keys()[vectorizer.vocabulary_.values().index(i)]
#         termandscore = [x[0],term]

#         higherscores.append(termandscore)
# scorefile = open('scorefile.txt', 'w')
# for y in sorted(higherscores,key=operator.itemgetter(0), reverse=True):
#     scorefile.write('%s\n' %(str(y)))
