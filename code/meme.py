from __future__ import division
import os
import networkx as nx
import re
import collections
import operator
import random
import codecs
from codecs import *
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS
import numpy as np
import re

import math
import pickle
import operator
from matplotlib import pyplot as plt

graph = nx.read_gexf('../data/echr-judgments-richmeta.gexf')
G = nx.read_gexf('../data/echr-judgments-richmeta.gexf')

articles_of_interest = [
 

'P1-1',
 '3']
# '6-1','6',]'2','10',
#'5-3',#'P1-1-1', '8', 
#'5',
 
 #'13',


for article in articles_of_interest:
	forplotf = []
	forplotp = []
	nodes = []
	for n in G.nodes_iter():
		if 'articles' in G.node[n]:
			if article in [x for x in re.split(r';|\+',G.node[n]['articles'])]:
				nodes.append(n)

	subgraph = G.subgraph(nodes)		
	edgelist = subgraph.edges()
	print edgelist
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
	    for file2 in filess if file2.endswith('noboiler') and 'jud_en' in directory and re.sub('_','/',directory.split('/')[-3]) in nodes]

	print 'files opened', len(files)


	cases = [re.sub('/','_',x) for x in files]
	files5 = []
	filenames = []
	for x in cases:
		dirs = os.listdir('../data/echr-copy-1/{}/jud_en'.format(x))
		#in case many judgments for that case number use most recent
		dir = max([int(y) for y in dirs])
		for f in os.listdir('../data/echr-copy-1/%s/jud_en/%s' %(x, dir)):
			if f.endswith('noboiler'):
				directory = '../data/echr-copy-1/%s/jud_en/%s' %(x, dir)
				files5.append(os.path.join(directory, f))
				filenames.append(re.sub('_','/',x))


	vectorizer = CountVectorizer(binary = True, input = 'filename', ngram_range=(3, 3),min_df=1, stop_words =ENGLISH_STOP_WORDS)
	vocab = vectorizer.fit_transform(files5)

	print 'vectorized'
	vocabtoarray = vocab.toarray()
	scorefile = open('re_trigram_scorefile_article_%s.txt' %(article))


	memescores = []


	for line in scorefile:
		strength,word = line.split(',')[0],line.split(',')[1]
		predictor = re.sub(r"(']|^\su')", "", word)
		pred =predictor[:-1]
		memeindex = vectorizer.vocabulary_[pred.decode('unicode-escape')]
		
		fileswmeme = [f for i,f in enumerate(filenames) if vocabtoarray[i][memeindex]]
		fwmset = set(fileswmeme)
		dmm = 0
		dmm2 = 0
		for f in fileswmeme:
			citing = [x for i,x in edgelist2 if i == f]
			
			if not fwmset.isdisjoint(citing):
				dmm+=1
			else:
				dmm2 +=1
		dm = 0
		dm2 = 0

		for f in filenames:
			citing = [x for i,x in edgelist2 if i == f]
			if not fwmset.isdisjoint(citing):
				dm+=1
			else:
				dm2 +=1
		noise = 3
		#print fileswmeme
		#print files5
		print dmm,dm,dmm2,dm2
		sticking = dmm/(dm + noise)
		sparking = (dmm2+noise )/(dm2 + noise)
		propagation= sticking/sparking
		frequency = len(fwmset)/len(filenames) #the ratio of publications carrying the meme
		memescore = propagation * frequency
		
		print pred, propagation, frequency
		print 'memescore= ', memescore,propagation,strength[1:], ' ', pred, article 
		
		forplotf.append(frequency)
		forplotp.append(propagation)

		memeandpred = [memescore,pred]
		memescores.append(memeandpred)
	# fig = plt.figure()	
	# plt.scatter(forplotf, forplotp)
	# fig.savefig('freqandmeme%s.png' %(article) )
	#commented out for testing	
	scorefile = open('re_trigam_memescorefile_article_%s.txt' %(article), 'w')
	
	for y in sorted(memescores,key=operator.itemgetter(0), reverse=True):
	    scorefile.write('%s\n' %(str(y)))
"""		
for every predictor:


	fileswmeme = [f for f in files if meme in f]

	fwmset = set(fileswmeme)
	dmm = 0
	for f in fileswmeme
		 if not fwmset.isdisjoint(f.nodes)
		 	dmm +=1
		 else:
		 	dmm2 +=1

	for f in files
		if not fwmset.isdisjoint(f.nodes)
			dm+=1
		else:
			dm2 +=1
"""
noise = 3

dmm = 1 #number of publications that carry the meme and cite at least one publication carrying the meme
dm = 2 #number of all publications (meme carrying or not) that cite at least one publication that carries the meme
sticking = dmm/dm + noise


dmm2 = 1 #number of meme-carrying publications that do not cite publications that carry the meme
dm2 = 2 #
sparking = dmm2+noise /dm2 + noise # number of all publications (meme carrying or not) that do not cite meme-carrying publications
propagation= sticking/sparking
frequency = 1/3 #the ratio of publications carrying the meme
memescore = propagation * frequency