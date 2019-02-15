

import networkx as nx
import re
import collections
import operator
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler, Normalizer
import random
import codecs
from codecs import *
import os
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS, TfidfVectorizer
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
from sklearn.feature_extraction import text 
from datetime import date
import datetime
from scipy import spatial
from itertools import combinations
from sklearn.metrics import roc_curve, auc
from scipy import sparse
import matplotlib.cm as cm
from sklearn.metrics import classification_report


def roc_plot(article,ystest, predictions, whichfeature, color2):

	false_positive_rate, true_positive_rate, thresholds = roc_curve(ystest, predictions)
	roc_auc = auc(false_positive_rate, true_positive_rate)
	plt.title('Receiver Operating Characteristic')
	plt.plot(false_positive_rate, true_positive_rate, color = color2,
	label='%d = %0.2f'% (whichfeature, roc_auc))
	plt.legend(loc='lower right')
	plt.plot([0,1],[0,1],'r--')
	plt.xlim([-0.1,1.2])
	plt.ylim([-0.1,1.2])
	plt.ylabel('True Positive Rate')
	plt.xlabel('False Positive Rate')
	plt.savefig('Article_%s_ROC' %(article))

def ngram_predictions(article,Xintersection,Xintersectiontest, ys, ystest, features, featurestest, combos, input = 'unigram'):
	colors = iter(cm.rainbow(np.linspace(0, 1, len(features)+1)))

	clf = LogisticRegression()
	clf.fit(Xintersection, ys)
	predictions = clf.predict(Xintersectiontest)
	
	print article,input, ' just intersection ' 
	print classification_report(predictions, ystest) 
	feat = 0
	#color = next(colors)
	#roc_plot(article,ystest, predictions, feat,color)

	for featurei,feature in enumerate(features):
		
		Xintersectionplus = [np.append(Xintersection[i], feature[i]) for i in range(len(feature))]
		clf2 = LogisticRegression()
		clf2.fit(Xintersectionplus, ys)
		Xintersectiontestplus = [np.append(Xintersectiontest[i], featurestest[featurei][i]) for i in range(len(featurestest[featurei]))]
		predictions = clf2.predict(Xintersectiontestplus)
		

		print article, input,' intersection and ',featurei
		print classification_report(predictions, ystest)
		#color = next(colors)
		#roc_plot(article, ystest, predictions, featurei, color)

	for featurecombo in [comb for comb in combos[1:] if len(comb)>1]:
		Xintersectionplus = Xintersection
		Xintersectiontestplus = Xintersectiontest
		for featur in featurecombo:
			newfeature = features[featur]
			newfeaturetest = featurestest[featur]
			Xintersectionplus = [np.append(Xintersectionplus[i], newfeature[i]) for i in range(len(newfeature))]
			Xintersectiontestplus =[np.append(Xintersectiontestplus[i], featurestest[featur][i]) for i in range(len(featurestest[featur]))]
			print len(Xintersectionplus[0])

		clf.fit(Xintersectionplus, ys)

		predictions = clf.predict(Xintersectiontestplus)	
		
		print article,input ,  ' intersection and ',featurecombo
		print classification_report(predictions, ystest)
		#roc_plot(ystest, predictions)

	for featurecombo in [comb for comb in combos[1:]]:
		Xintersectionplus = [[x] for x in features[featurecombo[0]]]
		Xintersectiontestplus = [[x] for x in featurestest[featurecombo[0]]]
		if len(featurecombo) > 1:
			for featur in featurecombo[1:]:
				newfeature = features[featur]
				newfeaturetest = featurestest[featur]
				Xintersectionplus = [np.append(Xintersectionplus[i], newfeature[i]) for i in range(len(newfeature))]
				Xintersectiontestplus =[np.append(Xintersectiontestplus[i], featurestest[featur][i]) for i in range(len(featurestest[featur]))]
				print len(Xintersectionplus[0])

		clf.fit(Xintersectionplus, ys)

		predictions = clf.predict(Xintersectiontestplus)	
		
		print article,input ,  'no intersection just ',featurecombo
		print classification_report(predictions, ystest)


articles_of_interest = [ '10','2',
'5-3',
'8-1', 
'14', 
'8', 
'P1-1-1', 
'5',
'3',   
'13',
'P1-1',
'6-1','6']

print 'STARTED'

graph = nx.read_gexf('../data/echr-judgments-richmeta.gexf')



G = nx.read_gexf('../data/echr-judgments-richmeta.gexf')
edgelist = G.edges()

for article in articles_of_interest:
	nodes = []
	for n in G.nodes_iter():
		if 'articles' in G.node[n]:
			if article in [x for x in re.split(r';|\+',G.node[n]['articles'])]:
				nodes.append(n)
	subgraph = G.subgraph(nodes)	
	#eigen = nx.eigenvector_centrality(subgraph)	
	h,a = nx.hits(subgraph)
	indegree = nx.in_degree_centrality(subgraph)
	edgelist = subgraph.edges()
	# for pair in edgelist:
	# 	print G.node[pair[1]]['date'], '%f' % (eigen[pair[1]]), '%f' %(a[pair[1]]), G.node[pair[0]]['date'], '%f' %(eigen[pair[0]]), '%f' %(a[pair[0]])
	print 'edgelist loaded', len(edgelist), 'len nodes', len(nodes), 'article: ', article
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

	vectorizer = CountVectorizer(binary = False, input = 'filename',min_df=4, stop_words =ENGLISH_STOP_WORDS)
	vocab = vectorizer.fit_transform(files5)
	vocabtoarray = vocab.toarray()
	usezero = np.zeros_like(vocabtoarray[0])

	vectorizerbigram = CountVectorizer(binary = False, input = 'filename', ngram_range=(2, 2),min_df=10, stop_words =ENGLISH_STOP_WORDS)
	vocabbigram = vectorizerbigram.fit_transform(files5)
	vocabtoarraybi = vocabbigram.toarray()
	usezerobi = np.zeros_like(vocabtoarraybi[0])

	vectorizertrigram = CountVectorizer(binary = False, input = 'filename', ngram_range=(3, 3),min_df=10, stop_words =ENGLISH_STOP_WORDS)
	vocabtrigram = vectorizertrigram.fit_transform(files5)
	vocabtoarraytri = vocabtrigram.toarray()
	usezerotri = np.zeros_like(vocabtoarraytri[0])
	print 'vectorized'
	tfidf = TfidfVectorizer(input = 'filename',stop_words =ENGLISH_STOP_WORDS).fit_transform(files5).toarray()
	
	
		
		
	    
	
	Xintersection = []


	Xintersectionbi = []

	Xintersectiontri = []

	date_format = "%Y-%m-%d"
	days = [(datetime.datetime.strptime('%s' %(G.node[pair[1]]['date']), date_format) - datetime.datetime.strptime('%s' %(G.node[pair[0]]['date']),date_format)).days 
			for i,pair in enumerate(onesandzeros)]

	samecountry = [1 if G.node[pair[0]]['respondent'] == G.node[pair[1]]['respondent'] else 0 for i,pair in enumerate(onesandzeros)]

	sharedarticles = [len(list(set([x for x in re.split(r';|\+',G.node[pair[0]]['articles'])]).intersection([x for x in re.split(r';|\+',G.node[pair[1]]['articles'])]))) 
			for i,pair in enumerate(onesandzeros)]

	importances = [G.node[pair[1]]['importance'] if  'importance' in G.node[pair[1]].keys() else '4' for i,pair in enumerate(onesandzeros)]

	cosines= []

	authorities = [a[pair[1]] for i,pair in enumerate(onesandzeros)]

	#eigens = [eigen[pair[1]] for i,pair in enumerate(onesandzeros)]

	indegrees = [indegree[pair[1]]  for i,pair in enumerate(onesandzeros)]

	
	ys = []

	
	traini = []
	testi= []
	for i,pair in enumerate(onesandzeros):
	    if i%500 ==0:	
	    	print i,' of ', len(onesandzeros)
	    indexa = filenames.index(pair[0])
	    indexb = filenames.index(pair[1])

	    usezero2 = usezero.copy()
	    indices= list(set(np.nonzero(vocabtoarray[indexa])[0]).intersection(np.nonzero(vocabtoarray[indexb])[0]))
	    intersects = np.put(usezero2,indices,1)

	    usezero2bi = usezerobi.copy()
	    indicesbi= list(set(np.nonzero(vocabtoarraybi[indexa])[0]).intersection(np.nonzero(vocabtoarraybi[indexb])[0]))
	    intersectsbi = np.put(usezero2bi,indicesbi,1)

	    usezero2tri = usezerotri.copy()
	    indicestri= list(set(np.nonzero(vocabtoarraytri[indexa])[0]).intersection(np.nonzero(vocabtoarraytri[indexb])[0]))
	    intersectstri = np.put(usezero2tri,indicestri,1)
	    Xintersection.append(usezero2)
	    Xintersectionbi.append(usezero2bi)
	    Xintersectiontri.append(usezero2tri)
	    if (i+1)*2 <= len(onesandzeros):
	    	ys.append(1)
	    else:
	    	ys.append(0)

	    cosines.append(1 - spatial.distance.cosine(tfidf[indexa], tfidf[indexb]))

	    if int(G.node[pair[0]]['date'].split('-')[0]) < 2012 or int(G.node[pair[1]]['date'].split('-')[0]) < 2012:
	    	traini.append(i)
	    else:
	    	testi.append(i)

	print len(Xintersection),  len(ys)
	print len(vectorizer.vocabulary_)

	#process features

	days = StandardScaler().fit_transform(days)
	sharedarticles = StandardScaler().fit_transform(sharedarticles)
	indegrees = StandardScaler().fit_transform(indegrees)

	importances1 = Normalizer().fit_transform(importances)
	cosines1 = Normalizer().fit_transform(cosines)
	authorities1 = Normalizer().fit_transform(authorities)
	#eigens1 = Normalizer().fit_transform(eigens)
	#split train test

	#load function properly
	
	print '**'
	print '**'
	print '**'
	print '**'
	print '**'
	print '**'
	print '**'
	features = [days,samecountry,sharedarticles,importances1,cosines1,authorities1,indegrees]
	print len(features[0])
	for f in features:
		print len(f)
		if len(f) == 1:
			print f
	featurestrain =[]
	featurestest = []
	for f in features: 
		ftrain = []
		ftest = []
		if len(f) !=1:
			for i in traini:
				ftrain.append(f[i])
			for it in testi:
				ftest.append(f[it])
		else:
			for it in testi:
				ftest.append(f[0][it])
			for i in traini:
				ftrain.append(f[0][i])
		featurestrain.append(ftrain)
		featurestest.append(ftest)


	Xintersectiontrain = [Xintersection[i] for i in traini]
	Xintersectiontest = [Xintersection[i] for i in testi]
	Xintersectiontrainbi =[Xintersectionbi[i] for i in traini]
	Xintersectiontestbi = [Xintersectionbi[i] for i in testi]
	Xintersectiontraintri =[Xintersectiontri[i] for i in traini]
	Xintersectiontesttri=[Xintersectiontri[i] for i in testi]
	ystrain = [ys[i] for i in traini]
	ystest = [ys[i] for i in testi]

	combos = sum([map(list, combinations(range(len(features)), i)) for i in range(len(features) + 1)], [])

	
	print len(Xintersectiontrain), len(ystrain)
	ngram_predictions(article,Xintersectiontrain,Xintersectiontest, ystrain, ystest, featurestrain, featurestest, combos, input = 'unigram')
	ngram_predictions(article, Xintersectiontrainbi,Xintersectiontestbi, ystrain, ystest, featurestrain, featurestest,combos, input = 'bigram')
	ngram_predictions(article, Xintersectiontraintri,Xintersectiontesttri, ystrain, ystest, featurestrain,featurestest, combos, input = 'trigram')
	#get train test split
	

	# clf2 = grid_search.GridSearchCV(estimator=clf,param_grid={"penalty":['l1','l2'],'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000]}, cv=5, n_jobs= 2, verbose = 10)
	# clf2.fit(Xintersection,ys)
	# print 'best score:  ',clf2.best_score_
	# print 'best estimator :  ', clf2.best_estimator_
	# print 'best parameter: ', clf2.best_params_
	# print 'test score after gridsearch: ', clf2.score(Xintersectiontest, ystest)