import networkx as nx
import re
import collections
import operator
from matplotlib import pyplot as plt
import random
import codecs
from codecs import *
import os
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS
import numpy as np
import re
import networkx as nx
import math
import pickle
import operator
from sklearn.linear_model import RandomizedLogisticRegression, LogisticRegression
from sklearn import grid_search
import tempfile
from sklearn.externals.joblib import Memory

# articles_of_interest = ['2',
# '5-3',
# '8-1', 
# '14', 
# '8', 
# 'P1-1-1', 
# '5',
# '3',   
# '13',
articles_of_interest= ['P1-1',
'6-1','6']
graph = nx.read_gexf('../data/echr-judgments-richmeta.gexf')



G = nx.read_gexf('../data/echr-judgments-richmeta.gexf')

for article in articles_of_interest:
	nodes = []
	for n in G.nodes_iter():
		if 'articles' in G.node[n]:
			if article in [x for x in re.split(r';|\+',G.node[n]['articles'])]:
				nodes.append(n)
	subgraph = G.subgraph(nodes)		
	edgelist = subgraph.edges()
	print 'edgelist loaded', len(edgelist), 'len nodes', len(nodes)
	usethislist = os.listdir('../data/echr-copy-1')
	edgelist2 = []

	'''
	make sure to remove the slicing here!!
	'''
	for pair in edgelist:
	    if re.sub('/', '_', pair[0]) in usethislist and re.sub('/', '_', pair[1]) in usethislist:
	        if 'jud_en' in os.listdir('../data/echr-copy-1/%s' %re.sub('/', '_', pair[0])) and 'jud_en' in os.listdir('../data/echr-copy-1/%s'% re.sub('/', '_', pair[1])):
	            edgelist2.append(pair)
	print 'edgelist modified for english only, and in actual data', len(edgelist2)


	files = [(re.sub('_','/',directory.split('/')[-3])) 
	    for directory, subs, filess in os.walk('../data/echr-copy-1')
	    for file2 in filess if file2.endswith('citations') and 'jud_en' in directory and re.sub('_','/',directory.split('/')[-3]) in nodes]

	print 'files opened', len(files)


	'''
	remove the slicing here
	'''
	percentage = 100
	sample = len(edgelist2) * int(percentage)/100
	print('going to load ys, sample is ', sample, ' pairs' )
	edgelist= edgelist2[0:sample]
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
	        if f.endswith('citations'):
	            directory = '../data/echr-copy-1/%s/jud_en/%s' %(x, dir)
	            files5.append(os.path.join(directory, f))
	            filenames.append(re.sub('_','/',x))
	print 'files appended'
	data = [edgelist,onesandzeros, cases, files5, filenames]
	# with open('preprocessed.pickle', "wb") as f:
	#     pickle.dump(data, f)

	vectorizer = CountVectorizer(binary = True, input = 'filename', min_df=4, stop_words =ENGLISH_STOP_WORDS)
	vocab = vectorizer.fit_transform(files5)
	print 'vectorized'
	vocabtoarray = vocab.toarray()
	usezero = np.zeros_like(vocabtoarray[0])
	print usezero
	Xintersection = []
	ys = []
	Xintersectiontest = []
	ystest = []
	for i,pair in enumerate(onesandzeros):
	    if i%500==0:	
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
	    if int(G.node[pair[0]]['date'].split('-')[0]) < 2013 or int(G.node[pair[1]]['date'].split('-')[0]) < 2013:
	        Xintersection.append(usezero2)
	        if (i+1)*2 <= len(onesandzeros):
	            ys.append(1)
	        else:
	            ys.append(0)
	    else:
	        Xintersectiontest.append(usezero2)
	        if (i+1)*2 <= len(onesandzeros):
	            ystest.append(1)
	        else:
	            ystest.append(0)
	        #print('indices put, and appended')
	print len(Xintersection), len(Xintersectiontest), len(ys), len(ystest)
	print len(vectorizer.vocabulary_)

	'''
	testing
	'''
	clf = LogisticRegression()
	clf.fit(Xintersection, ys)
	predictions = clf.predict(Xintersectiontest)
	for i, x in enumerate(predictions):
	    print x, ystest[i]

	print 'before gridsearch test score: ', clf.score(Xintersectiontest, ystest)
	# clf2 = grid_search.GridSearchCV(estimator=clf,param_grid={"penalty":['l1','l2'],'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000]}, cv=5, n_jobs= 2, verbose = 10)
	# clf2.fit(Xintersection,ys)
	# print 'best score:  ',clf2.best_score_
	# print 'best estimator :  ', clf2.best_estimator_
	# print 'best parameter: ', clf2.best_params_
	# print 'test score after gridsearch: ', clf2.score(Xintersectiontest, ystest)
	'''
	Stability selection
	'''

	cachedir = tempfile.mkdtemp()
	mem = Memory(cachedir=cachedir, verbose=1)

	selector = RandomizedLogisticRegression(n_resampling=100,random_state=101, memory =mem)
	Xintersection = Xintersection + Xintersectiontest
	ys = ys + ystest
	print(len(Xintersection[0]), len(Xintersection))
	selector.fit(Xintersection,ys)
	print(sum(selector.get_support() !=0))
	print(len(selector.all_scores_))
	print(len(vectorizer.vocabulary_))
	# with open('../data/Xs_Ys.pickle', 'wb') as handle:
	#   pickle.dump(Xintersection, handle)
	#   pickle.dump(ys, handle)
	higherscores = []
	for i,x in enumerate(selector.all_scores_):
	    if x != 0:
	        term = vectorizer.vocabulary_.keys()[vectorizer.vocabulary_.values().index(i)]
	        termandscore = [x[0],term]

	        higherscores.append(termandscore)
	scorefile = open('scorefile_article_%s.txt' %(article), 'w')

	for y in sorted(higherscores,key=operator.itemgetter(0), reverse=True):
	    scorefile.write('%s\n' %(str(y)))
