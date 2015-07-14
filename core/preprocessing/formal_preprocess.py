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


# in our case: filtered vector.bin with salient.csv (Segphrase output)
# this dictionary is used to align and filter phrases in the raw corpus
def build_phrase_dictionary(w2v_vector_file, output_dict_file, filter_file=None):
	with open(w2v_vector_file, 'r') as fin, open(output_dict_file, 'w') as fout:
		# create valid phrase dictionary
		valid_phrases = set()
		if filter_file != None:
			ffilter = open(filter_file, 'r')
			for line in ffilter:
				phrase = line.split(',')[0]
				valid_phrases.add(phrase)
			ffilter.close()

		# filter phrases accordng to this dictionary
		file_start = True
		phrase_id = 0
		for line in fin:
			if file_start:  # jump the first line
				file_start = False
				continue
			phrase = line.split()[0]
			if filter_file == None or (filter_file != None and phrase in valid_phrases):
				fout.write("{phrase} {phrase_id}\n".format(phrase=phrase, phrase_id=phrase_id))
				phrase_id += 1

"""
	example runs...
"""
# 一键生成topical phrases
def run_build_topic_hierarchy():
	seed_phrase_files = [PHRASE_DIST_PATH + '1dm-seed',
		PHRASE_DIST_PATH + '2ml-seed',
		PHRASE_DIST_PATH + '3db-seed',
		PHRASE_DIST_PATH + '4ir-seed']
	build_topic_hierarchy(DATA_PATH + 'keyphrase-vector-text-filtered.bin',
		seed_phrase_files,
		[1000] * len(seed_phrase_files),
		)

# 一键生成phrase dictionary
def run_build_phrase_dictionary():
	build_phrase_dictionary(DATA_PATH + 'keyphrase-vector-text-filtered.bin',
		DATA_PATH + 'id_phrase',
		)

if __name__ == '__main__':
	# run_build_topic_hierarchy()

	run_build_phrase_dictionary()