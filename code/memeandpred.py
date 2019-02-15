#!/usr/bin/env python
# -*- encoding: utf-8 -*-


import operator
import string
import re
from nltk.corpus import stopwords
from tabulate import tabulate


memescores= open('trigam_memescorefile_article_8.txt')
predicts = open('trigram_scorefile_article_8.txt')
guide = open('../data/guides/article8guide.pdf.txt')
g = guide.read()
#print article, guide.name
g2 = re.sub(r'(\b\w+)-\n(\w+\b)',r'\1\2',g)		
g2a = re.sub(r'(’|’s|“|”)','',g2)
g3 = g2a.translate(None, string.punctuation)
g4 = re.sub('\s+', ' ', g3)
g5 = ' '.join([word for word in g4.split() if word not in (stopwords.words('english'))])

guide = open('../data/guides/article8.pdf.txt')
g = guide.read()
#print article, guide.name
g2 = re.sub(r'(\b\w+)-\n(\w+\b)',r'\1\2',g)		
g2a = re.sub(r'(’|’s|“|”)','',g2)
g3 = g2a.translate(None, string.punctuation)
g4 = re.sub('\s+', ' ', g3)
g6 = ' '.join([word for word in g4.split() if word not in (stopwords.words('english'))])

g7 = g5 + g6


memes = []
preds = []
predscores = []
mscores = []
for line in memescores:
	strength,word = line.split(',')[0],line.split(',')[1]
	predictor = re.sub(r"(']|^\s')", "", word)
	score = re.sub(r"^\[", '', strength)
	pred =r'%s' %(predictor[:-1].decode('unicode-escape'))
	
	m =[pred,score]
	memes.append(pred)
	mscores.append(score)
for line in predicts:	
	strength,word = line.split(',')[0],line.split(',')[1]
	predictor = re.sub(r"(']|^\su')", "", word)
	score = re.sub(r"^\[", '', strength)
	pred =r'%s' %(predictor[:-1].decode('unicode-escape'))
	p = [pred,score]
	preds.append(pred)
	predscores.append(score)


together = []
togetherm = []
for i,x in enumerate(preds):
	if i <= 1000:
		hits = re.findall(x,g7 )
		
		firsttwo = x.split()[0] + ' ' + x.split()[1]
		lasttwo = x.split()[1] + ' ' + x.split()[2]
		onetwo = x.split()[0] + ' ' + x.split()[2]

		#print firsttwo
		hits2 = re.findall(firsttwo, g7)
		hits3 = re.findall(lasttwo, g7)
		hits4 = re.findall(onetwo, g7)
		if len(hits+hits2+hits3+hits4) == 0:
			if x in memes:
				if not bool(re.search(r'\d', x)):
					t = [x, i+memes.index(x)]
					together.append(t)

for i,x in enumerate(memes):
	if i <= 1000:
		hits = re.findall(x,g5 )
		
		firsttwo = x.split()[0] + ' ' + x.split()[1]
		lasttwo = x.split()[1] + ' ' + x.split()[2]
		onetwo = x.split()[0] + ' ' + x.split()[2]

		#print firsttwo
		hits2 = re.findall(firsttwo, g7)
		hits3 = re.findall(lasttwo, g7)
		hits4 = re.findall(onetwo, g7)
		if len(hits+hits2+hits3+hits4) == 0:
			if x in preds:
				if not bool(re.search(r'\d', x)):
					t = [x, i+preds.index(x)]
					togetherm.append(t)

together2 = [[x,score] for x,score in togetherm if x not in [y for y,s in together]]
t2 = sorted(together2+together, key=operator.itemgetter(1))
table = [str(x[1])+ ' '+x[0] for x in t2[:100]]
newtable = [[x, table[25:50][i], table[50:75][i], table[75:100][i] ]for i,x in enumerate(table[0:25])]
print tabulate(newtable, tablefmt="latex")

for x in t2[:100]:
	print x[0]