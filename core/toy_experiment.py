#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import numpy as np

import expert_finder.doc_meta as dm
import expert_finder.expert_finder as ef
import expert_finder.hits as hits
import expert_finder.build_hin as build_hin

DATA_PATH = os.path.dirname(__file__) + 'dataset/'
PHRASE_DIST_PATH = DATA_PATH + 'phrase_topic_dist/'
k = 3  # topic 0 plays as background topic
p = 27451  # 1-27451#
a = 9  # 1-8#
v = 10  # 1-9#

def generate_doc_meta_from_file(input_file):
    doc_meta_lst = []
    phrase_set = set()
    with open(input_file, 'r') as fin:
        papers = fin.read().split('\n\n')
        for paper in papers:
            attr = paper.split('\n')
            doc_id = int(attr[0])
            authors = set([int(a) for a in attr[1].split()])
            citations = set([int(d) for d in attr[2].split()])
            phrases = dict()
            for phrase_id in [int(p) for p in attr[3].strip().split()]:
                phrases.setdefault(phrase_id, 1)
                phrase_set.add(phrase_id)
            venue = int(attr[4])
            doc_meta_lst.append(dm.DocMeta(doc_id=doc_id,
                                phrases=phrases, authors=authors,
                                venue=venue, citations=citations))
    return (doc_meta_lst, phrase_set)

(docs, phrase_set) = generate_doc_meta_from_file(DATA_PATH + 'toy_corpus')

# back_ground_prob: the total probability of all phrases
# that do no appear input_file (should be very small)
def generate_phrase_topic_dist(input_file, tot_num_phrase, back_ground_prob):
    phrase_dist = [0] * tot_num_phrase
    num_topic_phrase = 0
    with open(input_file, 'r') as fin:
        norm_factor = 0.0
        for line in fin:
            phrase_info = line.strip().split()
            phrase_id, phrase_prob = int(phrase_info[1]), float(phrase_info[2])
            norm_factor += phrase_prob
            phrase_dist[phrase_id] = phrase_prob
            num_topic_phrase += 1
        
        non_topic_phrase_prob = back_ground_prob * 1.0 / (tot_num_phrase - num_topic_phrase)
        for phrase_id in xrange(tot_num_phrase):
            if phrase_id != 0:
                phrase_dist[phrase_id] = phrase_dist[phrase_id] / norm_factor * (1.0 - back_ground_prob)
            else:
                phrase_dist[phrase_id] = non_topic_phrase_prob
    return phrase_dist
    
# experiment 1.1
# test ExpertFinder's topic modeling works
def test_expert_finder_topic_modeling():
    alpha = np.ones(k)
    beta = np.ones(a)
    gamma = np.ones((k, v))
    omega = np.ones((k, p))
    toy_expert_finder = ef.ExpertFinder(
        K=k,
        docs_meta=docs,
        P=p,
        A=a,
        V=v,
        alpha=alpha,
        beta=beta,
        gamma=gamma,
        omega=omega,
        )
    ef.expert_finding_learning(toy_expert_finder, 3000)

# experiment 1.2
# test incorporiting with topic hierarchy
# will improve the result of author topic modeling
def test_expert_finder_hierarchy_rocks():
    alpha = np.ones(k) #may try different topic distribution
    beta = np.ones(a) #authors - uniform
    gamma = np.ones((k,v))
    back_phrase_prob = 1.0 / p
    background_topic_dist = [back_phrase_prob] * p
    fpm_topic_dist = generate_phrase_topic_dist(PHRASE_DIST_PATH + 'frequent_pattern_mining', 27451, 0.4)
    ds_topic_dist = generate_phrase_topic_dist(PHRASE_DIST_PATH + 'data_stream', 27451, 0.4)
    phrase_dist = [background_topic_dist, fpm_topic_dist, ds_topic_dist]
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
    ef.expert_finding_learning(toy_expert_finder, 3000)

# experiment 2.1
# test if HIN propagation works
# if it works, junk venues will be penalized
def test_expert_finder_hits():
    alpha = np.ones(k) #may try different topic distribution
    beta = np.ones(a) #authors - uniform
    gamma = np.array([[1,1,1,1,1,1,1,1,1,1],
                      [1,100,50,30,1,1,1,1,1,1],
                      [1,1,1,1,1,1,100,70,1,1]])
    back_phrase_prob = 1.0 / p
    background_topic_dist = [back_phrase_prob] * p
    fpm_topic_dist = generate_phrase_topic_dist(PHRASE_DIST_PATH + 'frequent_pattern_mining', 27451, 0.4)
    ds_topic_dist = generate_phrase_topic_dist(PHRASE_DIST_PATH + 'data_stream', 27451, 0.4)
    phrase_dist = [background_topic_dist, fpm_topic_dist, ds_topic_dist]

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
    ef.expert_finding_learning(toy_expert_finder, 200)

    toy_hin = build_hin.HIN(docs_meta=docs)
    toy_hits_1 = hits.HITS(toy_expert_finder, 1, toy_hin)
    #toy_hits_2 = bibrank.HITS(toy_expert_finder, 2, toy_hin)
    hits.propagate_with_hits(toy_hits_1, 300)
    #bibrank.propagate_with_hits(toy_hits_2, 300)
    print "auth papers"
    print toy_hits_1.auth_papers
    print "hub papers"
    print toy_hits_1.hub_papers
    print "auth authors"
    print toy_hits_1.auth_authors
    print "auth venues"
    print toy_hits_1.auth_venues

if __name__ == '__main__':
    #test_expert_finder_topic_modeling()
    #test_expert_finder_hierarchy_rocks()
    test_expert_finder_hits()
