#!/usr/bin/python
# -*- coding: utf-8 -*-

# build heterogenous information network
# Author: Hao Luo

from scipy.sparse import csr_matrix

from doc_meta import DocMeta


def parse_number(line):
	return int(line.split()[1])

#TODO: map conference to conference id = =
#TODO: add #！abtract to all papers
class HIN(object):
	def __init__(self, from_file=False, input_file=None, docs_meta=None, citation_dampen=0.2):
		# initialize csr_matrix constructor arguments
		indptr_d_d, indptr_d_a, indptr_d_v = [0], [0], [0]
		data_d_d, data_d_a, data_d_v = [], [], []
		indices_d_d, indices_d_a, indices_d_v = [], [], []
	
		# construct HIN cached DocMeta instances
		if not from_file:
			for doc_meta in docs_meta:
				# citations
				for citation in doc_meta.citations:
					indices_d_d.append(citation)
					if (doc_meta.authors & docs_meta[citation].authors):
						data_d_d.append(citation_dampen)
					else:
						data_d_d.append(1)
				# authors
				for author in doc_meta.authors:
					indices_d_a.append(author)
					data_d_a.append(1)
				# venue
				indices_d_v.append(doc_meta.venue)
				data_d_v.append(1)

				indptr_d_a.append(len(indices_d_a))
				indptr_d_d.append(len(indices_d_d))
				indptr_d_v.append(len(indices_d_v))

			# construct sparse adjacency matrices for 
			# paper-citation, paper-author, paper-venue relationships
			self.mat_d_a = csr_matrix((data_d_a, indices_d_a, indptr_d_a), dtype=float)
			self.mat_d_d = csr_matrix((data_d_d, indices_d_d, indptr_d_d), dtype=float)
			self.mat_d_v = csr_matrix((data_d_v, indices_d_v, indptr_d_v), dtype=float)

			self.mat_a_d = self.mat_d_a.transpose(copy=True)
			self.mat_d_d_t = self.mat_d_d.transpose(copy=True)
			self.mat_v_d = self.mat_d_v.transpose(copy=True)
			
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