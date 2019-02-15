
# # import numpy as np


# # from itertools import combinations
# # er,rea,ew = [1,2,3], [4,5,6], [7,8,9]
# # features = [er,rea,ew]
# # combos = sum([map(list, combinations(range(len(features)), i)) for i in range(len(features) + 1)], [])
# # print combos
# # for featurecombo in [comb for comb in combos[1:]]:
# # 	Xintersectionplus = [[x] for x in features[featurecombo[0]]]
# # 	print 'featurecombo', featurecombo
# # 	print 'base Xintersectionplus ', Xintersectionplus
# # 	if len(featurecombo) > 1:
# # 		for featur in featurecombo[1:]:
# # 			print 'feature ',featur
# # 			newfeature = features[featur]
# # 			Xintersectionplus = [np.append(Xintersectionplus[i], newfeature[i]) for i in range(len(newfeature))]
# # 			print ' new Xintersection ', Xintersectionplus
# count =0
# f = open('controversial.txt')
# for line in f:
# 	if '[' in line:
# 		count +=1
# 		print count

import collections
d = collections.defaultdict(dict)


for i in range(50):
	