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
from matplotlib import pyplot as plt


def comparefl(string,article, ngram = 1,scoref = 'tri'):
	print len(string)



	lawvectorizer = CountVectorizer(ngram_range=(ngram, ngram),min_df=6, stop_words =ENGLISH_STOP_WORDS)
	law_X = lawvectorizer.fit_transform(string)
	law_vocab = list(lawvectorizer.get_feature_names())
	
	law_counts = law_X.sum(axis=0).A1
	law_freq_distribution = Counter(dict(zip(law_vocab, law_counts)))
	scores = []
	counts = []
	if scoref == 'tri':
		with open('trigram_scorefile_article_%s.txt' %(article)) as sco:
			sc = sco.readlines()
			print len(sc), ' len scorefile'
			for line in sc:
				print line
				strength,word = line.split(',')[0],line.split(',')[1]
				predictor = re.sub(r"(']|^\su')", "", word)		
				print predictor[:-1],law_freq_distribution[predictor[:-1]]
				score = re.sub(r"^\[", '', strength)
				print score
				scores.append(score)
				counts.append(law_freq_distribution[predictor[:-1]])
			print scores
			print len(string)
			print '****'
			print '****'
			print '****'
			print '****'
			print counts
			plt.scatter(scores,counts)
			plt.show()
	else:
		pass
articles_of_interest = ['2',
'5-3',
'8-1', 
'14', 
'8', 
'P1-1-1', 
'5', '10']
# '3',   
# '13',
# 'P1-1',
# '6-1','6', '10']

print 'STARTED'

graph = nx.read_gexf('../data/echr-judgments-richmeta.gexf')



G = nx.read_gexf('../data/echr-judgments-richmeta.gexf')

for article in articles_of_interest:
	print article
	#scorefile = open('scorefile_article_%s.txt' %(article))
	


	# contro = open('controversial.txt')
	# con = contro.readlines()
	# terms = re.findall(r'\[\[([^\[]*)\]\]', ' '.join(con))
	# terms2 = [x.lower() for x in terms]

	# scores = []
	# counts = []
	# for line in scorefile:
	# 	strength,word = line.split(',')[0],line.split(',')[1]
	# 	predictor = re.sub(r"(']|^\su')", "", word)		
	# 	#print predictor[:-1]
	# 	score = re.sub(r"^\[", '', strength)
	# 	if predictor[:-1] in terms2:
	# 		print predictor, score
	# 		scores.append(score)
	filenames = []
	for n in G.nodes_iter():
		if 'articles' in G.node[n]:
			if article in [x for x in re.split(r';|\+',G.node[n]['articles'])]:
				
				filenames.append(re.sub('/', '_', n))
	stringfacts = []
	stringlaw = []
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
				#print re.split(r'(TO|\W) THE FACTS', c[0])
				if len(re.split(r'(TO|\W) THE FACTS', c[0])) >1 :
					afterfacts = re.split(r'(TO|\W) THE FACTS', c[0])[2]
					facts = afterfacts.split(' THE LAW')[0]
					if len(afterfacts.split(' THE LAW')) >1:
						law = afterfacts.split(' THE LAW')[1]
						stringfacts.append(facts)
						stringlaw.append(law)
	print len(stringfacts), len(stringlaw)
	
	comparefl(stringfacts,article, ngram = 3,scoref = 'tri')
	comparefl(stringlaw, article, ngram = 3,scoref = 'tri')
	# comparefl(scorefile,stringfacts, ngram =1 )	
	# comparefl(scorefile,  stringlaw,ngram =1)
	

	# word_freqs = Counter(regex.split(ur'', string))
	# print article
	# for w in word_freqs:
	# 	print w.decode('utf8'), word_freqs[w]

