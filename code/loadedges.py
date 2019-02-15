from __future__ import print_function
import random
import codecs
from codecs import *
import os
import numpy as np
import re
import networkx as nx
import math
import pickle
import operator



G = nx.read_gexf('../data/echr-judgments-richmeta.gexf')
edgelist =  G.edges()
print('edgelist loaded', len(edgelist))


usethislist = os.listdir('../data/echr-copy-1')
edgelist2 = []

'''
make sure to remove the slicing here!!
'''
for pair in edgelist:
    if re.sub('/', '_', pair[0]) in usethislist and re.sub('/', '_', pair[1]) in usethislist:
        if 'jud_en' in os.listdir('../data/echr-copy-1/%s' %re.sub('/', '_', pair[0])) and 'jud_en' in os.listdir('../data/echr-copy-1/%s'% re.sub('/', '_', pair[1])):
            edgelist2.append(pair)
print('edgelist modified for english only, and in actual data', len(edgelist2))


files = [(re.sub('_','/',directory.split('/')[-3]))
    for directory, subs, filess in os.walk('../data/echr-copy-1')
    for file2 in filess if file2.endswith('.txt') and 'jud_en' in directory]
print('files opened', len(files))

data = [edgelist2, files]
  with open('edgesandfiles.pickle', "wb") as f:
      pickle.dump(data, f)