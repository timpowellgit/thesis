import networkx as nx
import re
import collections
import operator
from matplotlib import pyplot as plt
import random
import codecs
from codecs import *
import os






G = nx.read_gexf('../data/echr-judgments-richmeta.gexf')
edgelist =  G.edges()
print 'edgelist loaded', len(edgelist)
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
    for directory, subs, filess in os.walk('/Users/timothypowell/thesis/data/echr-copy-1')
    for file2 in filess if file2.endswith('.txt') and 'jud_en' in directory]
print 'files opened', len(files)


'''



























