import os
import operator

from gensim.models import Word2Vec

DATA_PATH = os.path.dirname(__file__) + '../dataset/'
PHRASE_DIST_PATH = DATA_PATH + 'topical_phrase_dist/'

def extend_seed_phrases(model, input_file, topn, output_file, norm=False):
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
	norm_factor = sum(extend_phrases.values())
	with open(output_file, 'w') as fout:
		for phrase_score in sorted_phrases_score:
			score = phrase_score[1]
			if norm:
				score = score / norm_factor
			fout.write("{phrase} {score}\n".format(phrase=phrase_score[0], score=score))

def build_topic_hierarchy(w2v_model_file, seed_phrase_files, topns):
	w2v_model = Word2Vec.load_word2vec_format(w2v_model_file, binary=False)
	for idx, seed_phrase_file in enumerate(seed_phrase_files):
		extend_phrase_file = seed_phrase_file + '-ext'
		extend_seed_phrases(w2v_model, seed_phrase_file, topns[idx], extend_phrase_file)


if __name__ == '__main__':
	seed_phrase_files = [PHRASE_DIST_PATH + '1dm-seed',
		PHRASE_DIST_PATH + '2ml-seed',
		PHRASE_DIST_PATH + '3db-seed',
		PHRASE_DIST_PATH + '4ir-seed']
	build_topic_hierarchy(DATA_PATH + 'keyphrase-vector-text-filtered.bin',
		seed_phrase_files,
		[1000] * len(seed_phrase_files),
		)