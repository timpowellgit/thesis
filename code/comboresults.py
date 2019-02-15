import numpy as np
import collections
import re
classi = open('classificationreportall')
def rec_dd():
    return collections.defaultdict(rec_dd)
d = rec_dd()



total =0
article = None
ngram = None
combo = None
intersectin =  None
for line in classi:
	if 'intersection' in line:
		info = line.split()
		article = info[0]
		ngram = info[1]
		intersection = info[2]
		numbers =  re.findall('\d',' '.join(line.split()[1:]))
		print line
		combo = ''.join([x for x in numbers])
	print line
	if 'avg' in line:
		f1 = line.split()[-2]
		print f1,article,ngram, intersection, combo
		d[article][ngram][intersection][combo]=f1

example = d['2']['bigram']['no']
for key, value in example.iteritems():
	print key
print d['2']['bigram']['no']#['0']
print d['2']['bigram']['just']['']



for i in range(7):
	costs = []
	for key, value in example.iteritems():
		if str(i) in key and len(key) != 1:
			altkey = re.sub(str(i), '', key)
			#print i,key, example[key], altkey, example[altkey]
			costs.append(float(example[key]) -float(example[altkey]))
	print i, np.mean(costs)

def find_max(d, name=None):
    return max((v, k) if '.' in v else find_max(v, k) for k, v in d.items())

for article, ngramdict in d.iteritems():
	print ' '
	print "****ARTICLE**** ",article
	No = False
	for gram, interdict in ngramdict.iteritems():
		print '-----------',gram, '------------'
		
		for inter, combodict in interdict.iteritems():

			if inter != 'just' :
					
				print '++++++0101+++',inter, '++++01010++++'
				allfeatures = None
				maximum = max([value for key,value in combodict.iteritems()])
				
				print 'maximum', maximum,'just intersection ',interdict['just']['']
				print ' '
				for i in range(7):

					print i
					costs = []
					
					for key, value in combodict.iteritems():
						
						if len(key) == 6:
							allfeatures = combodict[key]
						if str(i) in key and len(key) != 1:
							altkey = re.sub(str(i), '', key)
							#print i,key, example[key], altkey, example[altkey]
							costs.append(float(combodict[key]) -float(combodict[altkey]))
						elif str(i) in key and len(key)== 1:
							print 'alone ', combodict[key]

					print  'cost', np.mean(costs)
				print 'all features ', allfeatures

			else:
				print 'ngram on its own ',interdict['just']['']





(9.0, 'nationwide')
