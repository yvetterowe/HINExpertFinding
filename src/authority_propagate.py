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
		self.hub_papers = np.ones(len(self.auth_papers))

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
	for i in xrange(iteration):
		hits.run()
