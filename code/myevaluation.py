import re
from matplotlib import pyplot as plt
from random import shuffle
import operator	
import numpy as np
f = open('re_trigram_scorefile_article_10.txt')
memefile = open('re_trigam_memescorefile_article_10.txt')
memes = []
memescores = []
for line in memefile:
	strength,word = line.split(',')[0][1:],line.split(',')[1][2:-3]
	print strength, word

	memes.append(word.decode('unicode-escape'))
	memescores.append(strength)
preds = []
strengths = []
for line in f:

	strength,word = line.split(',')[0],line.split(',')[1]
	predictor = re.sub(r"(']|^\su')", "", word)
	print predictor
	preds.append(predictor)
	strengths.append(strength[1:])

# shuffle(preds)
# for x in preds[0:500]:
# 	print x

f2 = open('myevalresults')

read = f2.readlines()
caselaw = []
notcaselaw = []
for i,x in enumerate(read):
	if i+1 < len(read):
		if read[i+1] != '\n' and read[i] != '\n':
			caselaw.append(x)

		else:
			if read[i] != '\n':
				notcaselaw.append(x)
for x in caselaw:
	print x
	if x in preds:
		print x , ' in new trigrams'
	else:
		print x, ' not in new trigrams'
positives = [strengths[preds.index(x)] for x in caselaw]
memepositives = [memescores[memes.index(x[:-1])] for x in caselaw]
negatives = [strengths[preds.index(x)] for x in notcaselaw]
memenegatives = [memescores[memes.index(x[:-1])] for x in notcaselaw]


#plot area under curve tricky add comments
#one axis is ranked pred strengths
#y axis is percentage of these preds that i identified as relevant
#do the same for meme scores

#first rank posis and negs together
joined = [ [x, strengths[preds.index(x)]] for x in caselaw + notcaselaw]
memesjoined = [ [x , memescores[memes.index(x[:-1])]] for x in caselaw + notcaselaw]
total = 0
numerator  = 0
percentage = 0
percentages = []


# mrank = memes.index(x)
# prank = preds.index(x)

# mscore = float(memescores[mrank])
# st = float(strengths[prank])

predsyepscores = []
predsnopescores = []
predsyepranks = []
predsnoperanks = []
for word,x in sorted(joined,key=operator.itemgetter(1), reverse=True):
	total +=1
	if word in caselaw:
		#print word, x
		numerator +=1
		predsyepscores.append(float(x))
		predsyepranks.append(preds.index(word))
	else:
		predsnopescores.append(float(x))
		predsnoperanks.append(preds.index(word))
		#print word, x , ' NOT CASEpredsnopescores.append(float(x)) LAW'
	percentage = numerator/float(total)
	percentages.append(percentage)


total1 = 0
numerator1  = 0
percentage1 = 0
percentages1 = []

memesyepscores = []
memesnopescores = []
memesyepranks = []
memesnoperanks = []
for word,x in sorted(memesjoined,key=operator.itemgetter(1), reverse=True):
	total1 +=1
	if word in caselaw:
		print word[:-1], x, ' CASE LAW!!!'
		numerator1 +=1
		memesyepscores.append(float(x))
		memesyepranks.append(memes.index(word[:-1]))
	else:
		e =1
		print word[:-1], x , ' NOT CASE LAW'
		memesnopescores.append(float(x))
		memesnoperanks.append(memes.index(word[:-1]))

	percentage1 = numerator1/float(total1)
	percentages1.append(percentage1)
	print percentage1

plt.plot(range(len(percentages)), percentages)

plt.plot(range(len(percentages1)), percentages1, 'r')
plt.show()

print 'avg score of identified preds',np.mean(predsyepscores)
print 'avg score of ignored preds',np.mean(predsnopescores)

print 'avg score of identified memes',np.mean(memesyepscores)

print 'avg score of ignored memes',np.mean(memesnopescores)
print 'avg rank of identified preds',np.mean(predsyepranks)
print 'avg rank of ignored preds',np.mean(predsnoperanks)

print 'avg rank of identified memes',np.mean(memesyepranks)

print 'avg rank of igored memes',np.mean(memesnoperanks)





