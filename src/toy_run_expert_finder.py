import os

import numpy as np

from authority_propagate import HITS, propagate_with_hits
from build_hin import HIN
from doc_meta import DocMeta
import expert_finder

DATA_PATH = os.path.dirname(__file__) + '../dataset/'
PHRASE_DIST_PATH = DATA_PATH + 'phrase_topic_dist/'

def generate_doc_meta_from_file(input_file):
	doc_meta_lst = []
	phrase_set = set()
	with open(input_file, 'r') as fin:
		papers = fin.read().split('\n\n')
		for paper in papers:
			attr = paper.split('\n')
			doc_id = int(attr[0])
			authors = set([int(a) for a in attr[1].split()])
			citations = set([int(d) for d in attr[2].split()])
			phrases = dict()
			for phrase_id in [int(p) for p in attr[3].strip().split()]:
				phrases.setdefault(phrase_id, 1)
				phrase_set.add(phrase_id)
			venue = int(attr[4])
			doc_meta_lst.append(DocMeta(
				doc_id=doc_id,
				phrases=phrases,
				authors=authors,
				venue=venue,
				citations=citations))
			#print "aha!"
	return doc_meta_lst, phrase_set

# back_ground_prob: the total probability of all phrases
# that do no appear input_file (should be very small)
def generate_phrase_topic_dist(input_file, tot_num_phrase, back_ground_prob):
	phrase_dist = [0] * tot_num_phrase
	num_topic_phrase = 0
	with open(input_file, 'r') as fin:
		norm_factor = 0.0
		for line in fin:
			phrase_info = line.strip().split()
			phrase_id, phrase_prob = int(phrase_info[1]), float(phrase_info[2])
			norm_factor += phrase_prob
			phrase_dist[phrase_id] = phrase_prob
			num_topic_phrase += 1
		
		non_topic_phrase_prob = back_ground_prob * 1.0 / (tot_num_phrase - num_topic_phrase)
		for phrase_id in xrange(tot_num_phrase):
			if phrase_id != 0:
				phrase_dist[phrase_id] = phrase_dist[phrase_id] / norm_factor * (1.0 - back_ground_prob)
			else:
				phrase_dist[phrase_id] = non_topic_phrase_prob
	return phrase_dist


def print_dict(dict_to_print, output_file):
    with open(output_file, 'w') as fout:
        for key, value in dict_to_print.items():
            fout.write("{key} {value}\n".format(
                key=key,
                value=value))


def check_phrase_dist(expert_finder, phrase_set):
	for phrase in phrase_set:
		phrase_dist = [expert_finder.dist_z_p[i][phrase] for i in xrange(expert_finder.K)]
		max_dist = max(phrase_dist)
		print phrase, phrase_dist.index(max_dist)


""" 
various toy experiments - show heuristics!!!
"""

# experiment 1.1
'''k = 3 #topic 0 plays as background topic
p = 27451 #1-27451#
a = 9 #1-8#
v = 10 #1-9#
alpha = np.ones(k) #may try different topic distribution
beta = np.ones(a) #authors - uniform
gamma = np.ones(v) #venue - uniform
omega = np.ones(p) #omega - '''

# experiment 1.2
'''k = 3 #topic 0 plays as background topic
p = 27451 #1-27451#
a = 9 #1-8#
v = 10 #1-9#
alpha = np.ones(k) #may try different topic distribution
beta = np.ones(a) #authors - uniform
gamma = np.ones(v) #venue - uniform
back_phrase_prob = 1.0 / p
background_topic_dist = [back_phrase_prob] * p
fpm_topic_dist = generate_phrase_topic_dist(PHRASE_DIST_PATH + 'frequent_pattern_mining', 27451, 0.4)
ds_topic_dist = generate_phrase_topic_dist(PHRASE_DIST_PATH + 'data_stream', 27451, 0.4)
phrase_dist = [background_topic_dist, fpm_topic_dist, ds_topic_dist]'''

# experiment 2.1
k = 3 #topic 0 plays as background topic
p = 27451 #1-27451#
a = 9 #1-8#
v = 10 #1-9#
alpha = np.ones(k) #may try different topic distribution
beta = np.ones(a) #authors - uniform
gamma = np.array([[1,1,1,1,1,1,1,1,1,1],
				  [1,100,50,30,1,1,1,1,1,1],
				  [1,1,1,1,1,1,100,70,1,1]
				  ]) #venue - each topic should have different prior...
back_phrase_prob = 1.0 / p
background_topic_dist = [back_phrase_prob] * p
fpm_topic_dist = generate_phrase_topic_dist(PHRASE_DIST_PATH + 'frequent_pattern_mining', 27451, 0.4)
ds_topic_dist = generate_phrase_topic_dist(PHRASE_DIST_PATH + 'data_stream', 27451, 0.4)
phrase_dist = [background_topic_dist, fpm_topic_dist, ds_topic_dist]

# structure data from raw text
docs, phrase_set = generate_doc_meta_from_file('toy_corpus')
toy_hin = HIN(from_file=False, docs_meta=docs)

# learn expert finder
# after this process, the topic ranking distribution are
# stored in the ExpertFinder instance
# these are the rough ranking score (first step score...)
toy_expert_finder = expert_finder.ExpertFinder(
	K=k,
	docs_meta=docs,
	P=p,
	A=a,
	V=v,
	alpha=alpha,
	beta=beta,
	gamma=gamma,
	#omega=omega,
	dist_phrase=phrase_dist,
	)
expert_finder.expert_finding_learning(toy_expert_finder, 3000)
#print "check final phrases"
#check_phrase_dist(toy_expert_finder, phrase_set)

# propagate authority score within each sub-topic (filter out false positive)
# after this process, the final score for each topic
# are store in HITS instantces (one instance per subtopic)
toy_hits_1 = HITS(toy_expert_finder, 1, toy_hin)
toy_hits_2 = HITS(toy_expert_finder, 2, toy_hin)
propagate_with_hits(toy_hits_1, 300)
propagate_with_hits(toy_hits_2, 300)
print toy_hits_1.auth_authors
