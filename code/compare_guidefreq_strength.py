#!/usr/bin/env python
# -*- encoding: utf-8 -*-


import os
import re
from matplotlib import pyplot as plt
from scipy.stats import pearsonr
import pickle
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import math
import string
from nltk.corpus import stopwords
import numpy as np
import operator
from pylab import *

def compare(meme = False):
	allfound = []
	allnotfound = []
	allfoundfreq = []
	allnotfoundfreq = []
	allcorpusfreq = []
	allscores = []
	if meme:
		scorefiles = [x for x in os.listdir(os.getcwd()) if 're_trigam_memescorefile_' in x]
	else:
		scorefiles = [x for x in os.listdir(os.getcwd()) if 're_trigram_scorefile_' in x]
		#scorefiles = [x for x in os.listdir(os.getcwd()) if x.startswith('scorefile_')]

	#print scorefiles
	for scorefile in scorefiles:
		article = scorefile.split(".")[0].split("_")[-1]
																																																																																																															
		try: 
			guide = open('../data/guides/article%sguide.pdf.txt' %(article))
			countdict = pickle.load( open( "trigram_countdict%s.pickle" %(article), "rb" ) )
			#countdict = pickle.load( open( "countdict%s.pickle" %(article), "rb" ) )

			totalvocab = sum([v for k,v in countdict.iteritems()])

			#print countdict
		except IOError as e:
			print e
			continue 
		g = guide.read()
		#print article, guide.name
		g2 = re.sub(r'(\b\w+)-\n(\w+\b)',r'\1\2',g)
		g2a = re.sub(r'(’|’s|“|”)','',g2)
		g3 = g2a.translate(None, string.punctuation)
		g4 = re.sub('\s+', ' ', g3)
		g5 = ' '.join([word for word in g4.split() if word not in (stopwords.words('english'))])
		#print g5
		allhits = []
		scores = []

		somescores = []
		somehits =[]

		found = []
		notfound = []

		corpusfreq = []
		f = open(scorefile)
		lines = f.readlines()
		for line in lines:
			strength,word = line.split(',')[0],line.split(',')[1]
			if not meme:
				predictor = re.sub(r"(']|^\su')", "", word)
				score = re.sub(r"^\[", '', strength)
				pred =r'%s' %(predictor[:-1].decode('unicode-escape'))
			else:
				predictor = re.sub(r"(']|^\s')", "", word)
				score = re.sub(r"^\[", '', strength)
				pred =r'%s' %(predictor[:-1].decode('unicode-escape'))
			hits = re.findall(pred,g5 )
			# firsttwo = pred.split()[0] + ' ' + pred.split()[1]
			# lasttwo = pred.split()[1] + ' ' + pred.split()[2]
			# hits2 = re.findall(firsttwo, g5)
			# hits3 = re.findall(lasttwo, g5)
			scores.append(float(score))
			allscores.append(float(score))
			#print float(countdict[pred/float(totalvocab))
			corpusfreq.append(float(countdict[pred]/float(totalvocab)))
			allcorpusfreq.append(float(countdict[pred]/float(totalvocab)))
			if len(hits) > 0:
				allhits.append(1)
				found.append(float(score))
				allfound.append((float(score),pred))
				allfoundfreq.append((float(countdict[pred]/float(totalvocab)),pred))
				
			else:
				allhits.append(0)
				notfound.append(float(score))
				allnotfound.append((float(score),pred))
				allnotfoundfreq.append((float(countdict[pred]/float(totalvocab)),pred))			
		
	
	return allfound ,allnotfound ,allfoundfreq ,allnotfoundfreq,allcorpusfreq ,allscores 


allfound ,allnotfound ,allfoundfreq ,allnotfoundfreq,allcorpusfreq ,allscores = compare(meme =False)

fig = plt.figure()	
ax = axes()
plt.boxplot([[x[0] for x in allfound ], [x[0] for x in allnotfound]])
ax.set_xticklabels(['Found', 'Not Found'])
plt.ylabel('Stability Selection Score') 
plt.show()
fig.savefig('predboxplots.png')

print np.median([x[0] for x in allfound ]), np.median([x[0] for x in allnotfound ])
print  np.percentile([x[0] for x in allfound ], 25),  np.percentile([x[0] for x in allnotfound ], 25)
print  np.percentile([x[0] for x in allfound ], 75),  np.percentile([x[0] for x in allnotfound ], 75)

fig2 = plt.figure()	
fig2 = plt.figure()	
plt.scatter([x[0] for x in allnotfound], [x[0] for x in allnotfoundfreq], s = 15,c = 'blue',alpha= 0.5,linewidths=0.001)
plt.scatter([x[0] for x in allfound ], [x[0] for x in allfoundfreq ],s = 15, c = 'red', alpha= 0.5, linewidths=0.001)
plt.xlim(-0.005, 1.05)
plt.xlabel('Stability Selection Score') 
plt.ylabel('Relative Frequency') 
#plt.ylim(-0.0001, 0.004)

plt.show()
fig2.savefig('predscatter.png')

# fig3 =plt.figure()
# nope = [[0,x,p] for x,p in allnotfound]
# yup = [[1,x,p] for x,p in allfound]
# yupnope = sorted(yup+nope,key=operator.itemgetter(1), reverse =True)
# percentages = []
# numerator = 0
# total = 0
# for i,x,p in yupnope:
# 	total +=1
# 	if i ==1:
# 		numerator +=1
# 	percentages.append(numerator/float(total))
# 	print numerator
# 	print numerator, '/ ',total, ' = ',   numerator/float(total), 'or ', numerator/total
# 	print numerator/float(total)
# #print yupnope
# plt.plot([i+1 for i,x in enumerate(yupnope)], percentages)
# #plt.show()

# allfreqs = allnotfoundfreq + allfoundfreq
# #allnotfoundfreq = [i for i,p in allnotfoundfreq]
# #allfoundfreq = [i for i,p in allfoundfreq]
# nopef = [[0,x,p] for x,p in allnotfoundfreq]
# yupf = [[1,x,p] for x,p in allfoundfreq]
# yupnopef = sorted(yupf+nopef,key=operator.itemgetter(1), reverse = True)
# percentagesf = []
# numeratorf = 0
# totalf = 0
# for i,x,p in yupnopef:
# 	totalf +=1

# 	if i ==1:
# 		numeratorf +=1
# 	percentagesf.append(numeratorf/float(totalf))
# 	print numeratorf/float(totalf)

# print yupnopef

# plt.plot([i+1 for i,x in enumerate(yupnopef)], percentagesf,'r')
# plt.xlabel('Rank by stability selection score') 
# plt.ylabel('Percentage found in literature')
# plt.show()
# fig3.savefig('predagreement.png')




fig4 =plt.figure()

nope = [[0,x,p] for x,p in allnotfound]
yup = [[1,x,p] for x,p in allfound]
yupnope = sorted(yup+nope,key=operator.itemgetter(1), reverse =True)

yn  =[yupnope[i:i + 271] for i in xrange(0, len(yupnope), 271)]

tobar = [len([1 for x in l if x[0]==1])/float(271)  for l in yn]
plt.bar(xrange(len(tobar)), tobar)
plt.xlabel('Ranked bins by stability selection score') 
plt.ylabel('Ngrams found in literature')
plt.show()
fig4.savefig('predbaruni.png')
# for i,x in enumerate(yn):
# 	print x
# 	print '**'
# 	print '**'
# 	print '**',i
# 	print '**'
# 	print '**'
# 	print '**'
# 	print '**'
# 	print '**'
# 	print '**'
# 	print '**'
# 	print '**'
# 	print '**'