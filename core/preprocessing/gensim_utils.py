import os
import operator

from gensim.models import Word2Vec

DATA_PATH = os.path.dirname(__file__) + '/../dataset/'
PHRASE_DIST_PATH = DATA_PATH + 'phrase_topic_dist/'


w2v_model_filtered = Word2Vec.load_word2vec_format(DATA_PATH + 'keyphrase-vector-text-filtered.bin', binary=False)


def extend_seed_phrases(model, input_file, topn, output_file):
	# read seed phrases
	seed_phrase_weights = dict()
	with open(input_file, 'r') as fin:
		for line in fin:
			phrase_weight = line.split()
			seed_phrase_weights[phrase_weight[0]] = float(phrase_weight[1])

	# extend
	extend_phrases = dict()
	for phrase, weight in seed_phrase_weights.items():
		sim_phrase_scores = model.most_similar(phrase, topn=topn) 
		for sim_phrase_score in sim_phrase_scores:
			phrase, score = sim_phrase_score[0], float(sim_phrase_score[1])
			phrase_weight = score * weight
			if not phrase in extend_phrases:
				extend_phrases[phrase] = phrase_weight
			else:
				extend_phrases[phrase] = max(extend_phrases[phrase], phrase_weight)

	# write output to file
	sorted_phrases_score = sorted(extend_phrases.items(), key=operator.itemgetter(1), reverse=True)
	norm = sum(extend_phrases.values())
	with open(output_file, 'w') as fout:
		for phrase_score in sorted_phrases_score:
			fout.write("{phrase} {score}\n".format(phrase=phrase_score[0], score=phrase_score[1]/norm))

extend_seed_phrases(w2v_model_filtered, PHRASE_DIST_PATH + '1dm-seed', 1000, PHRASE_DIST_PATH + '1dm-extend')
extend_seed_phrases(w2v_model_filtered, PHRASE_DIST_PATH + '2ml-seed', 1000, PHRASE_DIST_PATH + '2ml-extend')
extend_seed_phrases(w2v_model_filtered, PHRASE_DIST_PATH + '3db-seed', 1000, PHRASE_DIST_PATH + '3db-extend')
extend_seed_phrases(w2v_model_filtered, PHRASE_DIST_PATH + '4ir-seed', 1000, PHRASE_DIST_PATH + '4ir-extend')