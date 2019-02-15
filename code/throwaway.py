import random
import sys
import codecs
from codecs import *
from nltk.tokenize import word_tokenize, RegexpTokenizer
import os
from sklearn.feature_extraction.text import CountVectorizer
import itertools
import numpy as np
import re
import networkx as nx
import math
import pickle
import timeit

from sklearn.linear_model import RandomizedLogisticRegression
files = []
filenames = []
for dir, subd, filess in os.walk('../data/sample_chunk'):
    for file in filess:
        if file.endswith('txt'):
            files.append(codecs.open(os.path.join(dir,file), encoding='utf8'))
            filenames.append(dir.split('/')[3])
print filenames
vectorizer = CountVectorizer(binary = True, input = 'file', min_df=1)
vocab = vectorizer.fit_transform(files)
cases = []
for a,b in itertools.combinations(files, 2):
    cases.append((a.name.split('/')[3],b.name.split('/')[3]))
array = vocab.toarray()[1]
Xintersection= []
for a,b in cases:
    usezero = np.zeros_like(vocab.toarray()[0])
    indexa = filenames.index(a)
    indexb = filenames.index(b)
    indices= list(set(np.nonzero(vocab.toarray()[indexa])[0]).intersection(np.nonzero(vocab.toarray()[indexb])[0]))

    intersects = np.put(usezero,indices,1)
    Xintersection.append(usezero)

print Xintersection

