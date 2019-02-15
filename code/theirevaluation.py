import re
import numpy as np
from tabulate import tabulate

f = open('Article 10 ECHR Case Law.csv')
part2 = open('part2.csv')
f2 = f.readlines()
added = part2.readlines()



trigrams1 =  f2[0].split('","')[2:]
trigrams1[-1] ='incurred domestic proceedings'
henrik1 = f2[1].split('","')[2:]
henrik1[-1] = 'No'
anne1 = f2[2].split('","')[2:]
anne1[-1] = 'No'



trigrams2 =  added[0].split('","')[2:]
trigrams2[-1] ='measure legal protection'
henrik2 = added[1].split('","')[2:]
henrik2[-1] = 'No'
anne2 = added[2].split('","')[2:]
anne2[-1] = 'Yes'


trigrams = trigrams1 +trigrams2
henrik = henrik1 + henrik2
anne = anne1 + anne2

evaltrigrams = open('evaltrigrams.txt')
eval = evaltrigrams.readlines()


source = open('evaltrigramsshuffled.txt')
source2 = source.readlines()




uniq =[]
index = []
for i,x in enumerate(trigrams):

	if x not in uniq:
		pair = [i,x]
		uniq.append(x)
		index.append(i)
	


trigrams = uniq
anne = [anne[i] for i in index]
henrik = [henrik[i] for i in index]


topmemes = eval[50:100]
topmemes = [x[:-1] for x in topmemes]
toppreds = eval[0:50]
toppreds = [x[:-1] for x in toppreds]
indicesofmemes = [i for i,x in enumerate(trigrams) if x in topmemes]
indicesofpreds =  [i for i,x in enumerate(trigrams) if x in toppreds]

#remove trigrams that were not answered by both, check if in topmem

random = eval[100:]
random =[x[:-1] for x in random]
indicesofrandom = [i for i,x in enumerate(trigrams) if x in random and henrik[i] != '' and anne[i] != '']



indicesofagreement = [i for i,x in enumerate(henrik) if anne[i]==x]
agreement = len(indicesofagreement)/float(len(anne))

henrikmemes = [ i for i in indicesofmemes if henrik[i] == 'Yes']
print 'henrik meme percentage ',len(henrikmemes)/float(len(indicesofmemes))

annememes = [ i for i in indicesofmemes if anne[i] == 'Yes']
print 'anne meme percentage ',len(annememes)/float(len(indicesofmemes))



memeagreement = len([i for i in annememes if i in henrikmemes])/float(50)
print 'classified as memes in agreement ', memeagreement

overallmemeagreement = [i for i in range(50) if henrik[i] == anne[i]]
print 'overall meme agreement ',len(overallmemeagreement)/float(50)

henrikpreds = [ i for i in indicesofpreds if henrik[i] == 'Yes']
print 'henrik pred percentage ',len(henrikpreds)/float(len(indicesofpreds))

annepreds = [ i for i in indicesofpreds if anne[i] == 'Yes']
print 'anne pred percentage ',len(annepreds)/float(len(indicesofpreds))


predagreement = len([i for i in annepreds if i in henrikpreds])/float(50)
print 'classified as preds in agreement ',predagreement

overallpredagreement = [i for i in range(50,100) if henrik[i] == anne[i]]
print 'overall pred agreement ', len(overallpredagreement)/float(50)
# print len(indicesofpreds), len(indicesofmemes)


henrikrandom = [i for i in indicesofrandom if henrik[i] == 'Yes']
print 'henrik identified in random ',len(henrikrandom)/float(len(indicesofrandom))

annerandom = [i for i in indicesofrandom if anne[i] == 'Yes']
print 'anne identified in random ',len(annerandom)/float(len(indicesofrandom))

randomagreement = len([i for i in annerandom if i in henrikrandom])/float(len(indicesofrandom))

print 'agreement in those identified from random ',randomagreement

overallrandomagreement = [i for i in range(100, len(indicesofrandom)) if henrik[i] == anne[i]]
print 'agreement overall in random ',len(overallpredagreement)/float(len(indicesofrandom))
# print len(trigrams)
# print len(eval)
# print len(henrik)
# print henrik
# print trigrams
# print anne1


print ''
print ''
print ''
print ''

f = open('trigram_scorefile_article_10.txt')
memefile = open('trigam_memescorefile_article_10.txt')
memes = []
memescores = []
for line in memefile:
	strength,word = line.split(',')[0][1:],line.split(',')[1][2:-3]

	memes.append(word.decode('unicode-escape'))
	memescores.append(strength)
preds = []
strengths = []
for line in f:
	strength,word = line.split(',')[0],line.split(',')[1]
	predictor = re.sub(r"(']|^\su')", "", word)
	preds.append(predictor)
	strengths.append(strength[1:])
preds = [x[:-1] for x in preds]

memetable = []
for i,x in enumerate(topmemes):	

	if henrik[trigrams.index(x)] == 'Yes' and anne[trigrams.index(x)] == 'Yes':
		print i+1, x, ' *+*+'
		a = [str(i+1)+ ' ' + x+ ' *+*+']
		memetable.append(a)
	elif henrik[trigrams.index(x)] == 'Yes' and anne[trigrams.index(x)] == 'No':
		print i+1, x, ' +'
		a = [str(i+1)+ ' ' + x+ ' +']
		memetable.append(a)
	elif henrik[trigrams.index(x)] == 'No' and anne[trigrams.index(x)] == 'Yes':
		print i+1 , x ,' *'
		a = [str(i+1)+ ' ' + x+ ' *']
		memetable.append(a)
	elif henrik[trigrams.index(x)] == 'No' and anne[trigrams.index(x)] == 'No':
		print i+1 , x
		a = [str(i+1)+ ' ' + x]
		memetable.append(a)



print "-----"
print ' '

table = []

for i,x in enumerate(toppreds):	

	if henrik[trigrams.index(x)] == 'Yes' and anne[trigrams.index(x)] == 'Yes':
		print i+1, x, ' *+*+'
		a = [str(i+1)+ ' ' + x+ ' *+*+']
		table.append(a)
	elif henrik[trigrams.index(x)] == 'Yes' and anne[trigrams.index(x)] == 'No':
		print i+1, x, ' +'
		a = [str(i+1) + ' '+ x+ ' +']
		table.append(a)
	elif henrik[trigrams.index(x)] == 'No' and anne[trigrams.index(x)] == 'Yes':
		print i+1 , x ,' *'
		a = [str(i+1) + ' ' + x + ' *']
		table.append(a)
	elif henrik[trigrams.index(x)] == 'No' and anne[trigrams.index(x)] == 'No':
		print i+1 , x
		a = [str(i+1)+ ' ' + x]
		table.append(a)

print "-----"
print ' '


memerank = []
predrank = []
amrank = []
hmrank = []
aprank = []
hprank = []

nonemrank = []
noneprank = []

memez = []
predz = []
amz = []
hmz = []
apz = []
hpz = []

nonemz = []
nonepz = []

rtable = []

for i,x in enumerate(random):	
	mrank = memes.index(x)
	prank = preds.index(x)

	mscore = float(memescores[mrank])
	st = float(strengths[prank])
	if henrik[trigrams.index(x)] == 'Yes' and anne[trigrams.index(x)] == 'Yes':
		print  x, ' *+*+'
		a = [ x+ ' *+*+']
		rtable.append(a)
		memerank.append(mrank)
		predrank.append(prank)
		memez.append(mscore)
		predz.append(st)
	elif henrik[trigrams.index(x)] == 'Yes' and anne[trigrams.index(x)] == 'No':
		print  x, ' +'
		a = [ x+ ' +']
		rtable.append(a)
		hmrank.append(mrank)
		hprank.append(prank)
		hmz.append(mscore)
		hpz.append(st)
	elif henrik[trigrams.index(x)] == 'No' and anne[trigrams.index(x)] == 'Yes':
		print  x ,' *'
		a = [ x+ ' *']
		rtable.append(a)
		amrank.append(mrank)
		aprank.append(prank)
		amz.append(mscore)
		apz.append(st)
	elif henrik[trigrams.index(x)] == 'No' and anne[trigrams.index(x)] == 'No':
		print  x
		a = [ x]
		rtable.append(a)
		nonemrank.append(mrank)
		noneprank.append(prank)
		nonemz.append(mscore)
		nonepz.append(st)
print ' '
print 'avg meme rank BOTH', np.mean(memerank)
print 'avg pred rank BOTH',np.mean(predrank)
print 'avg meme rank anne',np.mean(amrank)
print 'avg pred rank anne',np.mean(aprank)
print 'avg meme rank henrik',np.mean(hmrank)
print 'avg pred rank henrik',np.mean(hprank)
print 'avg meme NOT rank BOTH',np.mean(nonemrank)
print 'avg pred NOT rank BOTH',np.mean(noneprank)
print ' '

print np.mean(memez)
print np.mean(predz)
print np.mean(amz)
print np.mean(apz)
print np.mean(hmz)
print np.mean(hpz)
print np.mean(nonemz)
print np.mean(nonepz)
print tabulate(table)


print table[0:25]
print table[25:]

newtable = [[x[0], table[12:24][i][0], table[24:36][i][0], table[36:48][i][0] ]for i,x in enumerate(table[0:12])]
print tabulate(newtable, tablefmt="latex")
newmtable = [[x[0], memetable[12:24][i][0], memetable[24:36][i][0], memetable[36:48][i][0] ]for i,x in enumerate(memetable[0:12])]

print tabulate(newmtable, tablefmt="latex")
print len(rtable)
newrtable = [[x[0], rtable[24:48][i][0], rtable[48:72][i][0], rtable[72:98][i][0] ]for i,x in enumerate(rtable[0:24])]


print tabulate(newrtable, tablefmt="latex")
