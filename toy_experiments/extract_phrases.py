import nltk
import os.path
from nltk.collocations import *

bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()

DATA_PATH = os.path.dirname(__file__) + '/../dataset/'

# change this to read in your data
bi_finder = BigramCollocationFinder.from_words(
   nltk.corpus.genesis.words(DATA_PATH + 'jiawei_han'))

tri_finder = TrigramCollocationFinder.from_words(
   nltk.corpus.genesis.words(DATA_PATH + 'jiawei_han'))
# only bigrams that appear 3+ times
bi_finder.apply_freq_filter(2) 
tri_finder.apply_freq_filter(2)

# return the 10 n-grams with the highest PMI
print bi_finder.nbest(bigram_measures.pmi, 15)
print tri_finder.nbest(trigram_measures.pmi, 15)
