import os.path

import numpy as np 

import doc_meta as dmeta

DATA_PATH = os.path.dirname(__file__) + '/../dataset/'
PHRASE_DIST_PATH = DATA_PATH + 'topical_phrase_dist/'
RESULT_PATH = os.path.dirname(__file__) + '/../../result/'
LOG_PATH = RESULT_PATH + 'logs/'
MODEL_PATH = RESULT_PATH + 'models/'

dict_file = {
	'author' : 'id_author',
	'venue' : 'id_venue',
}

"""
1. read corpus data (paper meta information)

file format (indexified):
	#index paper_id
	#@ author_id (seperated by space)
	#t paper_year
	#c paper_venue_id
	#% paper_citation_id
	#! paper_key_phrase_id (seperated by space)
"""
def read_data(input_file):
	doc_meta_lst = []
	with open(input_file, 'r') as fin:
		papers = fin.read().split('\n\n')
		for paper in papers:
			attr_lst = paper.split('\n')
			paper_id = int(attr_lst[0].split()[1])
			authors = [int(a) for a in attr_lst[1][3:].split()]
			year = int(attr_lst[2].split()[1])
			venue = int(attr_lst[3].split()[1])
			citations = set()
			for citation in attr_lst[4:-1]:
				citations.add(int(citation.split()[1]))
			phrases = dict()
			for phrase in attr_lst[-1][3:].split():
				phrases.setdefault(int(phrase), 1)
			doc_meta_lst.append(dmeta.DocMeta(
				doc_id=paper_id,
				phrases=phrases,
				authors=authors,
				venue=venue,
				citations=citations))
	return doc_meta_lst

def run_read_data():
	doc_meta_lst = read_data(DATA_PATH + 'AMiner-Paper-after1996-23venues-authorid-validcites-reindex-phrases.txt')
	print len(doc_meta_lst)
	for doc_meta in doc_meta_lst[:3]:
		print doc_meta.doc_id
		print doc_meta.phrases
		print "\n"

"""
2. read topical phrases and distribute the ranking scores through all vocabularies...
"""
def read_topical_phrase_dists(phrase_dist_files, phrase_dict_file, background_prob_lst, tot_num_phrase, use_background_topic=True):
	phrase_name_idx, phrase_idx_name = read_dictionary_file(phrase_dict_file)

	topical_phrase_dist = []
	for idx, phrase_dist_file in enumerate(phrase_dist_files):
		topical_phrase_dist.append(calc_topical_phrase_dist(
			phrase_dist_file,
			phrase_name_idx,
			background_prob_lst[idx],
			tot_num_phrase))
	if use_background_topic:
		topical_phrase_dist.append([1.0/tot_num_phrase] * tot_num_phrase)
	return topical_phrase_dist

# background_prob: the total probability of all phrases
# that do no appear input_file (should be very small)
# file format:
# 	phrase_dist_file: phrase score

def calc_topical_phrase_dist(phrase_dist_file, phrase_dict, background_prob, tot_num_phrase):
    phrase_dist = [0] * tot_num_phrase
    num_topic_phrase = 0
    with open(phrase_dist_file, 'r') as fin:
        norm_factor = 0.0
        for line in fin:
            phrase_info = line.strip().split()
            phrase_id, phrase_prob = phrase_dict[phrase_info[0]], float(phrase_info[1])
            norm_factor += phrase_prob
            phrase_dist[phrase_id] = phrase_prob
            num_topic_phrase += 1
        
        non_topic_phrase_prob = background_prob * 1.0 / (tot_num_phrase - num_topic_phrase)
        norm_factor = (1.0 - background_prob) / norm_factor
        for phrase_id in xrange(tot_num_phrase):
            if phrase_dist[phrase_id] != 0.0:
                phrase_dist[phrase_id] = phrase_dist[phrase_id] * norm_factor
            else:
                phrase_dist[phrase_id] = non_topic_phrase_prob
    return phrase_dist

def run_read_topical_phrase_dist():
	phrase_dist_files = [
		PHRASE_DIST_PATH + '1dm-seed-ext',
		PHRASE_DIST_PATH + '2ml-seed-ext',
		PHRASE_DIST_PATH + '3db-seed-ext',
		PHRASE_DIST_PATH + '4ir-seed-ext'
		]

	topical_phrase_dists = read_topical_phrase_dists(
		phrase_dist_files,
		[0.3] * len(phrase_dist_files),
		7566)


"""
3. read dictionary file
	file -> dict(key=id, value=name)
			and dict(key=name, value=id)
"""
def read_dictionary_file(input_file):
	name_idx_dict = dict()
	idx_name_dict = dict()
	with open(input_file, 'r') as fin:
		for line in fin:
			if not line:
				continue
			line_split = line.strip().split()
			name, idx = ' '.join(line_split[:-1]), int(line_split[-1])
			name_idx_dict[name] = idx
			idx_name_dict[idx] = name
	return name_idx_dict, idx_name_dict

"""
4. log writes to files...
"""
def log_ranking(dist_arr, log_type, iter_id, topn=50):
	name_idx_dict, idx_name_dict = read_dictionary_file(DATA_PATH + dict_file[log_type])
	num_topics = dist_arr.shape[0]
	for z in xrange(num_topics):
		log_topical_ranking(
			dist_arr[z], 
			log_type,
			z,
			idx_name_dict,
			iter_id,
			topn
			)

# log a single topic ranking
def log_topical_ranking(dist_arr, log_type, topic_label, idx_name_dict, iter_id, topn=20):
	if idx_name_dict == None:
		name_idx_dict, idx_name_dict = read_dictionary_file(DATA_PATH + dict_file[log_type])
	log_file_path = LOG_PATH + log_type + str(topic_label)
	with open(log_file_path, 'a') as fout:
		fout.write("iteration {iter}:\n".format(iter=iter_id))
		sorted_dist_arr_idx = np.argsort(dist_arr, axis=None)
		#print sorted_dist_arr_idx
		for i in xrange(topn):
			i_idx = sorted_dist_arr_idx[-1-i]
			i_name, i_score = idx_name_dict[i_idx], dist_arr[i_idx]
			fout.write("{name} {score}\n".format(name=i_name, score=i_score))
		fout.write('\n')


if __name__ == '__main__':
	#run_read_data()
	run_read_topical_phrase_dist()

