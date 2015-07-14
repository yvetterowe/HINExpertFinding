import os

import numpy as np

import hefbib.bibrank as bibrank
import hefbib.build_hin as bhin
import hefbib.doc_meta as dmeta
import hefbib.expert_finder as efinder
import hefbib.file_io as fio

def run_hefbib(input_corpus, 
	input_phrase_dists, 
	background_prob_lst,
	tot_num_topics,
	tot_num_phrases,
	tot_num_authors,
	tot_num_venues,
	ef_alpha, ef_beta, ef_gamma, ef_omega=None, ef_iter,
	br_iter,
	output_file):

	# read data 
	doc_meta_lst = fio.read_data(input_corpus)
	topical_phrase_dists = fio.read_topical_phrase_dists(
		input_phrase_dists,
		background_prob_lst,
		tot_num_phrases)
	
	# run ExpertFinder 
	expert_finder = efinder.ExpertFinder(
		K=tot_num_topics + 1,	# including background topic
        docs_meta=doc_meta_lst,
        P=tot_num_phrases,
        A=tot_num_authors,
        V=tot_num_venues,
        alpha=ef_alpha,
        beta=ef_beta,
        gamma=ef_gamma,
        omega=ef_omega,
        dist_phrase=topical_phrase_dists,
        )
	efinder.expert_finding_learning(expert_finder, ef_iter)

	# build global HIN
	hin = bhin.HIN(
		p=tot_num_phrases,
		a=tot_num_authors,
		v=tot_num_venues,
		docs_meta=doc_meta_lst,
		)

	# run BibRank for each topic (including background topic)
	for topic_label in xrange(tot_num_topics + 1):
		topic_bibrank = bibrank.BibRank(expert_finder,
			topic_label,
			hin,
			gamma_da=0.5,gamma_dv=0.5, gamma_dd=0.0,
			gamma_ad=1.0, gamma_aa=0.0)
		bibrank.propagte_with_bibrank(topic_bibrank, br_iter)

	# output results
	fio.write_results(bibrank, output_file)



if __name__ == '__main__':
	DATA_PATH = os.path.dirname(__file__) + 'dataset/'
	PHRASE_DIST_PATH = DATA_PATH + 'topical_phrase_dist/'
	
	input_phrase_dist = [
		PHRASE_DIST_PATH + '1dm-seed-ext',
		PHRASE_DIST_PATH + '2ml-seed-ext',
		PHRASE_DIST_PATH + '3db-seed-ext',
		PHRASE_DIST_PATH + '4ir-seed-ext'
	]
	
	run_hefbib(input_corpus=DATA_PATH + 'AMiner-Paper-after1996-23venues-authorid-validcites-reindex-phrases-index.txt', 
		input_phrase_dist=input_phrase_dist, 
		background_prob=[0.3] * 4,
		tot_num_topics=4,
		tot_num_phrases=5100,
		tot_num_authors=38491,
		tot_num_venues=23,
		ef_alpha=np.ones(5),  # always be tot_num_topics + 1
		ef_beta=np.ones(38491), 
		#ef_gamma=np.array([]), TODO : need some prior on venues, may read from file
		ef_omega=None, 
		ef_iter=2000,
		br_iter=300,
		output_file=DATA_PATH + 'logs/ahaha'):
