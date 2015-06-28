#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import expert_finder.build_hin as build_hin
import expert_finder.doc_meta as dm
from toy_experiment import generate_doc_meta_from_file

DATA_PATH = os.path.dirname(__file__) + 'dataset/'


def test_hin_basic_adj():
	(docs, phrase_set) = generate_doc_meta_from_file(DATA_PATH + 'toy_corpus_new')
	toy_hin = build_hin.HIN(docs_meta=docs)
	print toy_hin.m_d_a
	print toy_hin.m_d_v
	print toy_hin.m_d_d

def test_hin_weight_adj():
	doc1= dm.DocMeta(
		doc_id=0,
        phrases=dict(),
        authors=[1,2],
        venue=0,
        citations=set([1,2]),
        )
	doc2= dm.DocMeta(
		doc_id=1,
        phrases=dict(),
        authors=[0,1],
        venue=0,
        citations=set([2]),
        )
	doc3= dm.DocMeta(
		doc_id=2,
        phrases=dict(),
        authors=[2],
        venue=0,
        citations=set([1,0]),
        )
	toy_hin = build_hin.HIN(docs_meta=[doc1, doc2, doc3], a_d_norm_opt=2)
	print toy_hin.m_d_a.toarray()
	print toy_hin.m_a_d.toarray()


if __name__ == "__main__":
	#test_hin_basic_adj()
	test_hin_weight_adj()