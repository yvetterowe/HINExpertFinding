#!/usr/bin/python
# -*- coding: utf-8 -*-

# build heterogenous information network
# Author: Hao Luo

import numpy as np

from scipy.sparse import csr_matrix, csc_matrix
from sklearn.preprocessing import normalize

from doc_meta import DocMeta


def parse_number(line):
	return int(line.split()[1])

AUTHOR_ORDER_WEIGHT = {
	0:5,
	1:4,
	2:3,
	3:2,
	4:1,
}

#TODO: map conference to conference id = =
#TODO: add #！abtract to all papers
"""
Parameters:
	citation_dampen: the score authors receive for citing their own papers
	dense: True - adjacency matrices are dense. False - sparse.
	d_a_norm_opt: 0 - boolean value
				  1 - uniform normalized weights 
				  2 - weighted normalized weights
	a_d_norm_opt: 0 - boolean value
				  1 - uniform normalized weights (eg. all authors receives 1/n)
				  2 - weighted normalized weights (eg. first author receives 2/3
				  	and second author receives 1/3 of the paper authority score)
"""
class HIN(object):
	def __init__(self, p, a, v,
				 from_file=False, input_file=None, docs_meta=None,  
				 citation_dampen=0.2,
				 coauthor_thres = 4,
				 d_a_weighted_norm=True,
				 a_d_weighted_norm=True,
				 ):
		# initialize sparse matrix constructor arguments
		row_d_a, col_d_a, data_d_a = [], [], []
		row_d_v, col_d_v, data_d_v = [], [], []
		row_d_d, col_d_d, data_d_d = [], [], []
	
		# construct HIN cached DocMeta instances
		if not from_file:
			for doc_meta in docs_meta:
				# citations - m_d_d (被引用的paper - 引用它们的paper...)
				for citation in doc_meta.citations:				
					row_d_d.append(citation)
					col_d_d.append(doc_meta.doc_id)
					if set(doc_meta.authors) & set(docs_meta[citation].authors):
						data_d_d.append(citation_dampen)
					else:
						data_d_d.append(1)
				# authors m_d_a
				num_authors = len(doc_meta.authors)
				for idx, author in enumerate(doc_meta.authors):
					row_d_a.append(doc_meta.doc_id)
					col_d_a.append(author)
					if d_a_weighted_norm and idx < coauthor_thres:
						data_d_a.append(AUTHOR_ORDER_WEIGHT[idx])
					else:
						data_d_a.append(1)
				# venue m_d_v
				row_d_v.append(doc_meta.doc_id)
				col_d_v.append(doc_meta.venue)
				data_d_v.append(1)

			# construct sparse adjacency matrices for 
			# paper-author, paper-citation, paper-venue relationships
			d = len(docs_meta)
			self.m_d_a = csr_matrix((data_d_a, (row_d_a, col_d_a)), shape=(d,a), dtype=float)
			self.m_d_v = csr_matrix((data_d_v, (row_d_v, col_d_v)), shape=(d,v), dtype=float)		
			self.m_d_d = csr_matrix((data_d_d, (row_d_d, col_d_d)), shape=(d,d), dtype=float)		
			self.m_a_d = self.m_d_a.transpose(copy=True)		
			self.m_v_d = self.m_d_v.transpose(copy=True)
			#TODO
			self.m_a_a = np.ones((a,a))

			# normalize adjacency matrices
			self.m_d_a = normalize(self.m_d_a, norm='l1', axis=0)
			self.m_d_v = normalize(self.m_d_v, norm='l1', axis=0)
			self.m_d_d = normalize(self.m_d_d, norm='l1', axis=0)
			self.m_a_d = normalize(self.m_a_d, norm='l1', axis=0)	

	# TODO: save hin to file
	def save_to_file(output_file):
		with open(output_file) as fout:
			pass

	# TODO: read_from_file (static method???)