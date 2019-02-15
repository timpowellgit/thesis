import random
import codecs
from codecs import *
import os
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import re
import networkx as nx
import math
import pickle
import operator
from sklearn.linear_model import RandomizedLogisticRegression




G = nx.read_gexf('../data/echr-judgments-richmeta.gexf')
edgelist =  G.edges()
print 'edgelist loaded', len(edgelist)
usethislist = os.listdir('../data/echr-copy-1')
edgelist2 = []


'''
make sure to remove the slicing here!!
'''
for pair in edgelist[0:5000]:
    if re.sub('/', '_', pair[0]) in usethislist and re.sub('/', '_', pair[1]) in usethislist:
        if 'jud_en' in os.listdir('../data/echr-copy-1/%s' %re.sub('/', '_', pair[0])) and 'jud_en' in os.listdir('../data/echr-copy-1/%s'% re.sub('/', '_', pair[1])):
            edgelist2.append(pair)
print 'edgelist modified for english only, and in actual data', len(edgelist2)


files = [(re.sub('_','/',directory.split('/')[-3]))
    for directory, subs, filess in os.walk('/Users/timothypowell/thesis/data/echr-copy-1')
    for file2 in filess if file2.endswith('.txt') and 'jud_en' in directory]
print 'files opened', len(files)


'''
remove the slicing here
'''



edgelist= edgelist2[0:800]
zeros = []
while len(zeros) != len(edgelist):
    pair = tuple(random.sample(files, 2))
    
    if pair not in edgelist and pair not in zeros and tuple((pair[1],pair[0])) not in edgelist and tuple((pair[1],pair[0])) not in zeros:
        zeros.append(pair)
print 'cases sampled'
onesandzeros = edgelist+zeros



cases = [re.sub('/','_',x) for x in list(set(sum(onesandzeros, ())))]
print 'cases listed'
files5 = []
filenames = []
for i,x in enumerate(cases):
    dirs = os.listdir('../data/echr-copy-1/%s/jud_en' %(x))
    #in case many judgments for that case number use most recent
    dir = max([int(y) for y in dirs])
    for f in os.listdir('../data/echr-copy-1/%s/jud_en/%s' %(x, dir)):
        if f.endswith('.txt'):
            directory = '../data/echr-copy-1/%s/jud_en/%s' %(x, dir)
            files5.append(os.path.join(directory, f))
            filenames.append(re.sub('_','/',x))
print 'files appended'
data = [edgelist,onesandzeros, cases, files5, filenames]
with open('preprocessed.pickle', "wb") as f:
    pickle.dump(data, f)

vectorizer = CountVectorizer(binary = True, input = 'filename', min_df=1)
vocab = vectorizer.fit_transform(files5)
print 'vectorized'
vocabtoarray = vocab.toarray()
usezero = np.zeros_like(vocabtoarray[0])
print usezero
Xintersection = []
for i,pair in enumerate(onesandzeros):
    print i,' of ', len(onesandzeros)
    usezero2 = usezero.copy()
    
    #print(i, 'zeros loaded, to index now')
    indexa = filenames.index(pair[0])
    indexb = filenames.index(pair[1])
    #print('indexed gonna do the intersection now')
    indices= list(set(np.nonzero(vocabtoarray[indexa])[0]).intersection(np.nonzero(vocabtoarray[indexb])[0]))
    #print(indices)
    
    # for i in indices:
    #     for term, index in vectorizer.vocabulary_.iteritems():
    #         if index == i:
    #             print(term)

    #print('intersection found, gonna put the 1s at indices')
    intersects = np.put(usezero2,indices,1)
    
    Xintersection.append(usezero2)
    #print('indices put, and appended')
print len(Xintersection)
print len(vectorizer.vocabulary_)


selector = RandomizedLogisticRegression(n_resampling=300,random_state=101)
ys = [1 if (i+1)*2 <= len(onesandzeros) else 0 for i,x in enumerate(onesandzeros)]
print(len(Xintersection[0]), len(Xintersection))
selector.fit(Xintersection,ys)
print(sum(selector.get_support() !=0))
print(len(selector.all_scores_))
print(len(vectorizer.vocabulary_))
with open('../data/Xs_Ys.pickle', 'wb') as handle:
  pickle.dump(Xintersection, handle)
  pickle.dump(ys, handle)
higherscores = []
for i,x in enumerate(selector.all_scores_):
    if x != 0:
        term = vectorizer.vocabulary_.keys()[vectorizer.vocabulary_.values().index(i)]
        termandscore = [x[0],term]

        higherscores.append(termandscore)
scorefile = open('scorefile.txt', 'w')
for y in sorted(higherscores,key=operator.itemgetter(0), reverse=True):
    scorefile.write('%s\n' %(str(y)))



