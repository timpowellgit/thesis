from preprocessing import *
import codecs
from codecs import *
from nltk.tokenize import word_tokenize, RegexpTokenizer
import os
from sklearn.feature_extraction.text import CountVectorizer
import itertools


files = [codecs.open(os.path.join(directory, file), encoding = 'utf8')
    for directory, subs, files in os.walk('/Users/timothypowell/thesis/data/sample_chunk')
    for file in files
            if file.endswith('citations.txt')]

vectorizer = CountVectorizer(binary = True, input = 'file', min_df=1)
print files
X = vectorizer.fit_transform(files)
print X.toarray()
names =  vectorizer.get_feature_names()

# for x in X.toarray():
#     print vectorizer.inverse_transform(x)
for a, b in itertools.combinations(X.toarray(), 2):
    first = vectorizer.inverse_transform(a)
    second = vectorizer.inverse_transform(b)
    #print first
    #print first[0]
    #print set(first)
    u = list(set.intersection(set(first[0]),set(second[0])))
    vectorizer.input = 'content'
    print vectorizer.transform(u)
'''
tokenizer = RegexpTokenizer(r'\w+')
vocab = []
tokens_docs = []
for directory, subs, files in os.walk('/Users/timothypowell/thesis/data/echr-copy-1'):
    for file in files:

        if file.endswith('citations.txt'):
            with codecs.open(os.path.join(directory, file), encoding = 'utf8') as f:
                read = f.read()
                #cleaned = html2text(read)
                #print cleaned
                tokens = tokenizer.tokenize(read)
                stemmed = stemming(tokens, type = 'PorterStemmer')
                vocab += stemmed
                tokens_docs.append(stemmed)
                print len(vocab)

vocab = set(vocab)
print len(vocab)
word_to_id = {token: idx for idx, token in enumerate(vocab)}
token_ids = [[word_to_id[token] for token in tokens_doc] for tokens_doc in tokens_docs]

vec = OneHotEncoder(n_values=len(word_to_id))
X = vec.fit_transform(token_ids)
with open('filename.pickle', 'wb') as handle:
  pickle.dump(a.toarray, handle)

'''