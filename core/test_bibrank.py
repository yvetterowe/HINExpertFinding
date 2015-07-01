#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pprint

import numpy as np

import expert_finder.doc_meta as dm
import expert_finder.expert_finder as ef
import expert_finder.bibrank as bibrank
import expert_finder.build_hin as build_hin
from test_expertfinder import generate_doc_meta_from_file, generate_phrase_topic_dist

DATA_PATH = os.path.dirname(__file__) + 'dataset/'
PHRASE_DIST_PATH = DATA_PATH + 'phrase_topic_dist/'


# the following experiments are
# conducted 
k = 2 
p = 27451 
a = 6 
v = 3

(docs, phrase_set) = generate_doc_meta_from_file(DATA_PATH + 'toy_corpus_new')
toy_hin = build_hin.HIN(p=p, a=a, v=v, docs_meta=docs)

alpha = np.ones(k) #may try different topic distribution
beta = np.ones(a) #authors - uniform
gamma = np.array([[1,1,1],
    		     [100,1,1]])
back_phrase_prob = 1.0 / p
background_topic_dist = [back_phrase_prob] * p
fpm_topic_dist = generate_phrase_topic_dist(PHRASE_DIST_PATH + 'frequent_pattern_mining', 27451, 0.4)
phrase_dist = [background_topic_dist, fpm_topic_dist]

toy_expert_finder = ef.ExpertFinder(
		K=k,
        docs_meta=docs,
        P=p,
        A=a,
        V=v,
        alpha=alpha,
        beta=beta,
        gamma=gamma,
        dist_phrase=phrase_dist,
        )
#ef.expert_finding_learning(toy_expert_finder, 3000)

def format_list(lst, num_col):
	num_row = len(lst) / num_col
	return '\n'.join([(' '.join([str(round(x,3)) for x in lst[i*num_col:(i+1)*num_col]])) for i in xrange(num_row)])

def print_result(bibrank):
	print "auhors: \n{author_rank}".format(author_rank=bibrank.rank_authors)
	print "venues: \n{venue_rank}".format(venue_rank=bibrank.rank_venues)
	print "papers:"
	print format_list(bibrank.rank_papers, 10)

# experiment 2.2
def test_bibrank_junk_venue_sucks():
	toy_bibrank = bibrank.BibRank(toy_expert_finder, 1, toy_hin,
								  gamma_da=0.5,gamma_dv=0.5, gamma_dd=0.0,
    							  gamma_ad=1.0, gamma_aa=0.0)

	bibrank.propagte_with_bibrank(toy_bibrank, 250)
	print_result(toy_bibrank)

# experiment 2.3 - 2.6
def test_bibrank_cite_own_paper_sucks():
	toy_bibrank = bibrank.BibRank(
		toy_expert_finder, 1, toy_hin,
		gamma_da=0.4, gamma_dv=0.4, gamma_dd=0.2,
		gamma_ad=1.0, gamma_aa=0.0)
	bibrank.propagte_with_bibrank(toy_bibrank, 250)
	print_result(toy_bibrank)


if __name__ == "__main__":
    test_bibrank_junk_venue_sucks()	
    #test_bibrank_cite_own_paper_sucks()
