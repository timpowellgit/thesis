from __future__ import print_function
import codecs
from codecs import *
from nltk.tokenize import word_tokenize, RegexpTokenizer
import os
from sklearn.feature_extraction.text import CountVectorizer
import itertools
import numpy as np
import re
import networkx as nx
import math
import pickle
import timeit

G = nx.read_gexf('../data/echr-judgments-richmeta.gexf')
edgelist =  G.edges()

print('edgelist loaded')


files = [codecs.open(os.path.join(directory, file), encoding = 'utf8')
    for directory, subs, filess in os.walk('/Users/timothypowell/thesis/data/sample_chunk')
    for file in filess
            if file.endswith('citations.txt')]

print('files opened')


vectorizer = CountVectorizer(binary = True, input = 'file', min_df=1)
X = vectorizer.fit_transform(files)
print('vectorized')

Xintersection = []
ys = []
n= len(files)

f = math.factorial
nCr = f(n) / f(2) / f(n-2)
print('factorial calculated')

casenos= [(re.sub('_','/',files[a[0]].name.split('/')[-4]),print(a[0], ' of ', len(files)))[0] for a in enumerate(X.toarray())]
print('cases compiled')
count = 1





def forloop(r):


    ys = []
    for i, pair in enumerate(itertools.combinations(enumerate(X.toarray()), r)):
        ys.append(1 if ((casenos[pair[0][0]], casenos[pair[1][0]]) in edgelist)
                                     or ((casenos[pair[1][0]], casenos[pair[0][0]]) in edgelist)
        else 0)

    return ys

def listcomp(r):
    return [1 if ((casenos[pair[0][0]], casenos[pair[1][0]]) in edgelist)
                                      or ((casenos[pair[1][0]],casenos[pair[0][0]]) in edgelist)
      else 0
      for i, pair in
      enumerate(itertools.combinations(enumerate(X.toarray()), r))]

setedge = [frozenset(y) for y in edgelist]

def listcompset(r):
    return [1 if (set((casenos[pair[0][0]], casenos[pair[1][0]])) in setedge)

      else 0
      for i, pair in
      enumerate(itertools.combinations(enumerate(X.toarray()), r))]


cases = [frozenset((casenos[pair[0][0]], casenos[pair[1][0]])) for i, pair in
      enumerate(itertools.combinations(enumerate(X.toarray()), 2))]

def listcompsetcases(r):
    return [1 if cases[i] in setedge

      else 0
      for i, pair in
      enumerate(itertools.combinations(enumerate(X.toarray()), r))]

combos = [(i,pair) for i, pair in
      enumerate(itertools.combinations(enumerate(X.toarray()), 2))]

def listcompsetcasescombos():
    return [1 if cases[i] in setedge

      else 0
      for i, pair in
      combos]

def numper():
    return cases.index(list(set(cases).intersection(setedge))[0])

def compprint(r):
    return [(1,print(i, ' of ', nCr))[0] if ((casenos[pair[0][0]], casenos[pair[1][0]]) in edgelist)
                                      or ((casenos[pair[1][0]],casenos[pair[0][0]]) in edgelist)
      else (0,print(i, ' of ', nCr))[0]
      for i, pair in
      enumerate(itertools.combinations(enumerate(X.toarray()), r))]

fortimed =timeit.timeit('f(2)', 'from __main__ import forloop as f',number=10)
comptimed = timeit.timeit('f(2)', 'from __main__ import listcomp as f', number=10)
compprinttimed = timeit.timeit('f(2)', 'from __main__ import compprint as f', number=10)
settimed = timeit.timeit('f(2)', 'from __main__ import listcompset as f', number=10)
casessettimed = timeit.timeit('f(2)', 'from __main__ import listcompsetcases as f', number=10)
casessetcombotimed = timeit.timeit('f()', 'from __main__ import listcompsetcasescombos as f', number=10)
numpertimed = timeit.timeit('f()', 'from __main__ import numper as f', number=10)
print(fortimed,comptimed, compprinttimed, settimed, casessettimed, casessetcombotimed)

#
# ys =[(1,print(i, ' of ', nCr))[0] if ((casenos[pair[0][0]], casenos[pair[1][0]]) in edgelist)
#                                       or ((casenos[pair[1][0]],casenos[pair[0][0]]) in edgelist)
#       else (0,print(i, ' of ', nCr))[0]
#       for i, pair in
#       enumerate(itertools.combinations(enumerate(X.toarray()), 2))]
# print(ys)
#use itertool combinations to match all possible combinations
# for a, b in itertools.combinations(enumerate(X.toarray()), 2):
#     print count, ' of ', nCr
#     count +=1
#
#
#     #add 1 or 0 according to whether tuple is there, as in if edge between nodes exists
#     if ((casenos[a[0]], casenos[b[0]]) in edgelist) or ((casenos[b[0]],casenos[a[0]]) in edgelist):
#         ys.append(1)
#     else:
#         ys.append(0)
    # first = vectorizer.inverse_transform(a[1])
    # second = vectorizer.inverse_transform(b[1])
    #
    #
    # u = list(set.intersection(set(first[0]),set(second[0])))
    # vectorizer.input = 'content'
    # intersection = vectorizer.transform(u).toarray()[0]
    # intersection = intersection.tolist()
    # Xintersection.append(intersection)


with open('../data/Xs_Ys.pickle', 'wb') as handle:
  pickle.dump(Xintersection, handle)
  pickle.dump(ys, handle)


'''
tokenizer = RegexpTokenizer(r'\w+')
vocab = []
tokens_docs = []
for directory, subs, files in os.walk('/Users/timothypowell/thesis/data/echr-copy-1'):
    for file in files:

        if file.endswith('citations.txt'):
            with codecs.open(os.path.join(directory, file), encoding = 'utf8') as f:
                read = f.read()
                #cleaned = html2text(read)
                #print cleaned
                tokens = tokenizer.tokenize(read)
                stemmed = stemming(tokens, type = 'PorterStemmer')
                vocab += stemmed
                tokens_docs.append(stemmed)
                print len(vocab)

vocab = set(vocab)
print len(vocab)
word_to_id = {token: idx for idx, token in enumerate(vocab)}
token_ids = [[word_to_id[token] for token in tokens_doc] for tokens_doc in tokens_docs]

vec = OneHotEncoder(n_values=len(word_to_id))
X = vec.fit_transform(token_ids)
with open('filename.pickle', 'wb') as handle:
  pickle.dump(a.toarray, handle)

'''