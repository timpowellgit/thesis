import os
import re 
from random import shuffle




if yes:
23
bullshit varibales syntax errors so i dont accidentally run this code again = e 45

#create file with all trigrams mixed
#create file with memes and preds separated
#make sure no duplicates in random selections
alltrigrams = []

f = open('trigram_scorefile_article_10.txt')
preds = []
for line in f:
	strength,word = line.split(',')[0],line.split(',')[1]
	predictor = re.sub(r"(']|^\su')", "", word)
	preds.append(predictor)
for x in preds[0:50]:
	alltrigrams.append(x)


f2 = open('trigam_memescorefile_article_10.txt')
memes = []
for line in f2:
	strength,word = line.split(',')[0],line.split(',')[1]
	predictor = re.sub(r"(']|^\su')", "", word)
	memes.append(predictor)	
for x in memes[0:50]:
	alltrigrams.append(x[2:])

print alltrigrams
print len(alltrigrams), len(set(alltrigrams))


shuffle(preds)
shuffle(memes)
uniquepreds = []
for x in preds:
	if x not in alltrigrams and len(uniquepreds) != 50:
		uniquepreds.append(x)

for x in uniquepreds:
	alltrigrams.append(x)

print len(uniquepreds), len(alltrigrams), len(set(alltrigrams))			
print '$$$$$$$$$$$$$$$$'


print len(alltrigrams), len(set(alltrigrams))
shuffle(memes)
print '********'

uniquememes = []

for x in memes:
	if x[2:] not in alltrigrams and len(uniquememes) !=50:
		uniquememes.append(x[2:])
		
for x in uniquememes:
	alltrigrams.append(x)
print len(alltrigrams), len(set(alltrigrams))

#remove duplicates from top 50s of meme and preds

with open('evaltrigrams.txt', 'w') as t:
	for x in alltrigrams:
		t.write(x.strip()+'\n')

shuffle(alltrigrams)
list(set(alltrigrams))
with open('evaltrigramsshuffled.txt', 'w') as t1:
	for x in alltrigrams:
		t1.write(x.strip()+'\n')
