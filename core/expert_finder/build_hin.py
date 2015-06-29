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

#TODO: map conference to conference id = =
#TODO: add #！abtract to all papers
"""
Parameters:
	citation_dampen: the score authors receive for citing their own papers
	dense: True - adjacency matrices are dense. False - sparse.
	d_a_norm_opt: 0 - only boolean value
				  1 - uniform normalized weights (eg. )
				  2 - (TODO: for noamlized weights according to co-author order)
	a_d_norm_opt: 0 for boolean value
				  1 for uniform normalized weights (eg. all authors receives 1/n)
				  2 for weighted normalize eights (eg. first author receives 2/3
				  	and second author receives 1/3 of the paper authority score)
"""
class HIN(object):
	def __init__(self, p, a, v,
				 from_file=False, input_file=None, docs_meta=None,  
				 citation_dampen=0.2,
				 d_a_norm_opt=1,
				 a_d_norm_opt=2,
				 ):
		# initialize csr_matrix constructor arguments
		indptr_d_d, indptr_d_a, indptr_d_v = [0], [0], [0]
		data_d_d, data_d_a, data_d_v = [], [], []
		indices_d_d, indices_d_a, indices_d_v = [], [], []
		row_a_d, col_a_d, data_a_d = [], [], []
		row_d_d, col_d_d, data_d_d = [], [], []
	
		# construct HIN cached DocMeta instances
		if not from_file:
			for doc_meta in docs_meta:
				# citations - m_d_d
				for citation in doc_meta.citations:
					#indices_d_d.append(citation)
					col_d_d.append(doc_meta.doc_id)
					row_d_d.append(citation)
					if set(doc_meta.authors) & set(docs_meta[citation].authors):
						data_d_d.append(citation_dampen)
					else:
						data_d_d.append(1)
				# authors m_d_a & m_a_d
				num_authors = len(doc_meta.authors)
				for idx, author in enumerate(doc_meta.authors):
					# m_d_a
					indices_d_a.append(author)
					data_d_a.append(1)
					# m_a_d
					col_a_d.append(doc_meta.doc_id)
					row_a_d.append(author)
					if a_d_norm_opt in [0,1]:
						data_a_d.append(1)
					else:
						data_a_d.append(num_authors - idx)					
				# venue m_d_v
				indices_d_v.append(doc_meta.venue)
				data_d_v.append(1)

				indptr_d_a.append(len(indices_d_a))
				#indptr_d_d.append(len(indices_d_d))
				indptr_d_v.append(len(indices_d_v))

			# construct sparse adjacency matrices for 
			# paper-author, paper-citation, paper-venue relationships
			d = len(docs_meta)
			self.m_d_a = csr_matrix((data_d_a, indices_d_a, indptr_d_a), shape=(d,a), dtype=float)
			self.m_d_v = csr_matrix((data_d_v, indices_d_v, indptr_d_v), shape=(d,v), dtype=float)
			#self.m_d_d = csr_matrix((data_d_d, indices_d_d, indptr_d_d), shape=(d,d), dtype=float)
			self.m_d_d = csc_matrix((data_d_d, (row_d_d, col_d_d)), shape=(d,d), dtype=float)
			self.m_a_d = csc_matrix((data_a_d, (row_a_d, col_a_d)), shape=(a,d), dtype=float)
			self.m_v_d = self.m_d_v.transpose(copy=True)
			#TODO
			self.m_a_a = np.ones((a,a))

			if d_a_norm_opt == 1:
				self.m_d_a = normalize(self.m_d_a, norm='l1', axis=0)
			if a_d_norm_opt != 0:
				self.m_a_d = normalize(self.m_a_d, norm='l1', axis=0)		
			return

		# TODO: construct HIN directly from file
		assert input_file != None
		with open(input_file) as fin:
			papers = fin.read().split('\n\n')
			for paper in papers:
				attrs = paper.split('\n')
				doc_id = parse_number(attrs[0])
				#title attrs[1]
				authors = set([int(a) for a in attrs[2].split()[1:]])
				year = parse_number(attrs[3])
				venue = parse_number(attr[4])
				#phrases = dict{phrase_id:cnt}
				#citations = 

			self.mat_d_d = csr_matrix([]) # paper-citation adjacency matrix
			self.mat_d_a = csr_matrix([]) # paper-author adjacency matrix
			self.mat_d_v = csr_matrix([]) # paper-venue adjacency matrix

			self.mat_d_d_t = self.mat_d_d.transpose(copy=True)
			self.mat_a_d = self.mat_d_a.transpose(copy=True)
			self.mat_v_d = self.mat_d_v.transpose(copy=True)

	# TODO: save hin to file
	def save_to_file(output_file):
		with open(output_file) as fout:
			pass

	# TODO: read_from_file (static method???)