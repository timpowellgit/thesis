#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import re 
import nltk
import os
import networkx as nx
import glob
import regex
from collections import Counter
from nltk import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS
import pickle
articles_of_interest = ['2',
'5-3',
'8-1', 
'14', 
'8', 
'P1-1-1', 
'5',
'3',   
'13',
'P1-1',
'6-1','6', '10']

print 'STARTED'

graph = nx.read_gexf('../data/echr-judgments-richmeta.gexf')



G = nx.read_gexf('../data/echr-judgments-richmeta.gexf')

for article in articles_of_interest:
	filenames = []
	for n in G.nodes_iter():
		if 'articles' in G.node[n]:
			if article in [x for x in re.split(r';|\+',G.node[n]['articles'])]:
				
				filenames.append(re.sub('/', '_', n))
	string = ' '
	files= []
	for f in filenames:
		gl= glob.glob(r'../data/echr-copy-1/%s/jud_en/*/*nocitations' %(f))
		max =0
		for path in gl:
			year = path.split('/')[5][:4]
			if year> max:
				max = year
		gl2 = glob.glob(r'../data/echr-copy-1/%s/jud_en/%s*/*nocitations' %(f,max))
		if len(gl2) > 0:
			rightpath = gl2[0]
			files.append(rightpath)
			with open(rightpath) as opened:
				c =opened.readlines()

				string += c[0]
	ngram_vectorizer = CountVectorizer(input = 'filename',ngram_range=(3, 3),min_df=6, stop_words =ENGLISH_STOP_WORDS)
	# X matrix where the row represents sentences and column is our one-hot vector for each token in our vocabulary
	X = ngram_vectorizer.fit_transform(files)

	# Vocabulary
	vocab = list(ngram_vectorizer.get_feature_names())

	# Column-wise sum of the X matrix.
	# It's some crazy numpy syntax that looks horribly unpythonic
	# For details, see http://stackoverflow.com/questions/3337301/numpy-matrix-to-array
	# and http://stackoverflow.com/questions/13567345/how-to-calculate-the-sum-of-all-columns-of-a-2d-numpy-array-efficiently
	counts = X.sum(axis=0).A1
	freq_distribution = Counter(dict(zip(vocab, counts)))

	with open('trigram_countdict%s.pickle' %(article), "wb") as d:
	    pickle.dump(freq_distribution, d)


	# word_freqs = Counter(regex.split(ur'', string))
	# print article
	# for w in word_freqs:
	# 	print w.decode('utf8'), word_freqs[w]

