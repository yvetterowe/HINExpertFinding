#!/usr/bin/python
# -*- coding: utf-8 -*-

# authority propagation with HITS 
# Author: Hao Luo

import numpy as np
from sklearn.preprocessing import normalize

from build_hin import HIN

# helper functions -- TODO: move to a seperated module
def norm_vector(vector):
	norm = np.linalg.norm(vector)
	if norm:
		return vector / norm
	else:
		return vector

def zerolize_vector(vector, thres):
    return np.array([i if i >= thres else 0.0 for i in vector])

def clean_vector(vector, thres):
	return zerolize_vector(norm_vector(vector), thres)


class HITS(object):
	def __init__(self, expert_finder, topic_label, hin, thres=0.1):
		# reference to global hin
		self.hin = hin

		# authority and hub scores (np.array)
		self.auth_papers = np.array([1 if z == topic_label else 0 
									 for z in expert_finder.z_d])
		self.auth_authors = clean_vector(expert_finder.dist_z_a[topic_label], thres)
		self.auth_venues = clean_vector(expert_finder.dist_z_v[topic_label], thres)
		#self.hub_papers = np.ones(len(self.auth_papers))
		self.hub_papers = norm_vector(
							self.hin.mat_d_d.dot(self.auth_papers) + \
		                  	self.hin.mat_d_a.dot(self.auth_authors) + \
		                  	self.hin.mat_d_v.dot(self.auth_venues))

	def run(self):
		# update authority scores
		self.auth_papers = norm_vector(self.hin.mat_d_d_t.dot(self.hub_papers))
		self.auth_authors = norm_vector(self.hin.mat_a_d.dot(self.hub_papers))
		self.auth_venues = norm_vector(self.hin.mat_v_d.dot(self.hub_papers))
		# update hub scores
		self.hub_papers = norm_vector(
							self.hin.mat_d_d.dot(self.auth_papers) + \
		                  	self.hin.mat_d_a.dot(self.auth_authors) + \
		                  	self.hin.mat_d_v.dot(self.auth_venues))

def propagate_with_hits(hits, iteration):
	fout = open('prop_out', 'w')
	for i in xrange(iteration):
		fout.write("iter {i}\n".format(i=i))
		fout.write("{dist}\n".format(dist=hits.auth_authors))
		hits.run()
	fout.close()


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