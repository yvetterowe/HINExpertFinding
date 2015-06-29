#!/usr/bin/python
# -*- coding: utf-8 -*-

# authority propagation with BibRank
# Author: Hao Luo

import numpy as np

class BibRank(object):
	def __init__(self, expert_finder, topic_label, hin,
				 eps_d=0.8, eps_a=0.6, eps_v=0.8,
				 gamma_da=1.0/3, gamma_dv=1.0/3, gamma_dd=1.0/3,
				 gamma_ad=1.0/2, gamma_aa=1.0/2,
				 ):
		# propagation factor should sum up to 1
		assert gamma_da + gamma_dv + gamma_dd == 1.0
		assert gamma_ad + gamma_aa == 1.0
		self.eps_d, self.eps_a, self.eps_v = eps_d, eps_a, eps_v
		self.gamma_da, self.gamma_dv, self.gamma_dd = gamma_da, gamma_dv, gamma_dd
		self.gamma_ad, self.gamma_aa = gamma_ad, gamma_aa

		# reference to global hin
		self.hin = hin

		# initial topical rank scores of papers, authors and venues
		# two strategies: 
		#    1) either 1 or 0 
        #    2) topical ranking distributino inferred from ExpertFinder
		#self.init_rank_papers = np.array([1 if z == topic_label else 0 
		#							      for z in expert_finder.z_d])
		#self.init_rank_authors = expert_finder.dist_z_a[topic_label]
		#self.init_rank_venues = expert_finder.dist_z_v[topic_label]
		self.init_rank_papers = np.array([1] * len(expert_finder.z_d))
		self.init_rank_authors = np.array([0.166] * 5 + [0.166])
		self.init_rank_venues = np.array([0.75, 0.25, 0.1])
		print "initial authors: ", self.init_rank_authors
		print "initial venues: ", self.init_rank_venues

		# iterative rank scores of papers, authors and venues
		self.rank_papers = self.init_rank_papers
		self.rank_authors = self.init_rank_authors
		self.rank_venues = self.init_rank_venues

	def run(self):
		last_rank_papers = self.rank_papers
		self.rank_papers = self.eps_d * self.init_rank_papers + \
						   (1 - self.eps_d) * (self.gamma_da * self.hin.m_d_a.dot(self.rank_authors) + 
						   					   self.gamma_dv * self.hin.m_d_v.dot(self.rank_venues) + 
						   	                   self.gamma_dd * self.hin.m_d_d.dot(last_rank_papers))
		self.rank_authors = self.eps_a * self.init_rank_authors + \
							(1 - self.eps_a) * (self.gamma_ad * self.hin.m_a_d.dot(last_rank_papers) + 
								                self.gamma_aa * self.hin.m_a_a.dot(self.rank_authors))
		self.rank_venues = self.eps_v * self.init_rank_venues + \
						   (1 - self.eps_v) * self.hin.m_v_d.dot(last_rank_papers)

def format_list(lst, num_col):
	num_row = len(lst) / num_col
	return '\n'.join([(' '.join([str(round(x,3)) for x in lst[i*num_col:(i+1)*num_col]])) for i in xrange(num_row)])

def propagte_with_bibrank(bibrank, iteration):
	fout_paper = open('bibrank_log_paper', 'w')
	fout_author = open('bibrank_log_author', 'w')
	fout_venue = open('bibrank_log_venue', 'w')
	for i in xrange(iteration):
		fout_paper.write("iter {i}\n".format(i=i))
		fout_author.write("iter {i}\n".format(i=i))
		fout_venue.write("iter {i}\n".format(i=i))
		#fout.write("author: {rank}\n".format(rank=bibrank.rank_authors))
		#fout.write("venue: {rank}\n\n".format(rank=bibrank.rank_venues))
		#fout.write("papers: {rank}\n\n".format(rank=bibrank.rank_papers))
		fout_paper.write("{rank}\n\n".format(rank=format_list(bibrank.rank_papers, 10)))
		fout_author.write("{rank}\n\n".format(rank=bibrank.rank_authors))
		fout_venue.write("{rank}\n\n".format(rank=bibrank.rank_venues))
		bibrank.run()
	fout_paper.close()
	fout_author.close()
	fout_venue.close()