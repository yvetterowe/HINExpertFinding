from gensim.models import Word2Vec, Phrases
#from nltk.corpus import brown, treebank

#w2v_model = Word2Vec(treebank.sents())
#w2v_model.save('w2v_treebank')
'''w2v_model = Word2Vec.load('w2v_treebank') # w2v_model is a dictionary (key=word, value=feature vector)

print w2v_model.most_similar('money', topn=5)

#phrase_model = Phrases(treebank.sents())
#phrase_model.save('phrase_treebank')
phrase_model = Phrases.load('phrase_treebank') # phrase_model is a dictionary (key=sentence with single tokens, value=sentence with phrases combined)
sample_sent = [u'Pierre', u'Vinken', u',', u'61', u'years', u'old',
			   u',', u'will', u'join', u'the', u'board', u'as', u'a', 
			   u'nonexecutive', u'director', u'Nov.', u'29', u'.']
print phrase_model[sample_sent]

#w2v_phrase_model = Word2Vec(phrase_model[treebank.sents()])
#w2v_phrase_model.save('w2v_phrase_treebank')
w2v_phrase_model = Word2Vec.load('w2v_phrase_treebank')'''

print "test wor2vec with text8 demo"
w2v_tex8_model = Word2Vec.load('vectors.bin')
print w2v_tex8_model.most_similar('china', topn=10)