#!/usr/bin/python
# -*- coding: utf-8 -*-

# authority propagation with BibRank
# Author: Hao Luo

class BibRank(object):
	def __init__(self, expert_finder, topic_label, hin
				 eps_d=0.8, eps_a=0.8, eps_v=0.8,
				 gamma_da=1/3, gamma_dv=1/3, gamma_dd=1/3,
				 gamma_ad=1/2, gamma_aa=1/2,
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
		self.init_rank_papers = np.array([1 if z == topic_label else 0 
									      for z in expert_finder.z_d])
		self.init_rank_authors = self.hin.mat_z_a[topic_label]
		self.init_rank_venues = self.hin.mat_z_v[topic_label]

		# iterative rank scores of papers, authors and venues
		self.rank_papers
		self.rank_authors
		self.rank_venues

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

def propagte_with_bibrank(bibrank, iteration):
	for i in xrange(iteration):
		bibrank.run()