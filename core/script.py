#import numpy as np
#from scipy.sparse import csr_matrix
#from sklearn.preprocessing import normalize
#import random
import re

import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.datasets import fetch_20newsgroups
from textblob import TextBlob

'''count_vect = CountVectorizer()
twenty_train = ["aaa bbb ccc aaa", "aaa ccc ddd ddd ddd"]
X_train_counts = count_vect.fit_transform(twenty_train)

print X_train_counts.toarray() 
print "word count:"
print count_vect.vocabulary_
print count_vect.vocabulary_[u'aaa']

tfidf_vect = TfidfVectorizer()
idf = tfidf_vect.fit_transform(twenty_train)
print "idf"
print tfidf_vect.idf_
print "sorted_index"
y = np.argsort(tfidf_vect.idf_)[::-1]

print "vocab"
print tfidf_vect.vocabulary_
print tfidf_vect.get_feature_names()
for word in y:
	print tfidf_vect.get_feature_names()[word]'''

x = "aaa bbb ccc 1345"
print ' '.join(x.split()[:-1])