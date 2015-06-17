#!/usr/bin/python
# -*- coding: utf-8 -*-

# ExpertFinder + collapsed Gibbs sampling
# Author: Hao Luo

import numpy as np

from doc_meta import DocMeta


class ExpertFinder(object):

    def __init__(self, K, docs_meta, P, A, V,
    	alpha, beta, gamma, omega=None,
        dist_phrase=None,smartinit=False,
        ):
        self.K = K
        self.alpha = alpha  # hyperparameter for topics prior
        self.beta = beta  # hyperparameter for authors prior
        self.gamma = gamma  # hyperparameter for venues prior
        self.docs_meta = docs_meta
        self.P = P
        self.A = A
        self.V = V

        self.n_z = np.zeros(K) + alpha  # paper count for each topic
        self.n_z_a = np.zeros((K, A)) + beta  # paper count for each topic and author
        self.n_z_v = np.zeros((K, V)) + gamma  # paper count for each topic and venue
        self.z_d = np.empty(len(docs_meta))  # topic for each paper

        self.dist_z_a = np.array([np.random.dirichlet(beta) for z in
                                 xrange(K)])
        self.dist_z_v = np.array([np.random.dirichlet(gamma) for z in
                                 xrange(K)])

        self.dist_z_p = dist_phrase
        self.infer_dist_phrase = False
        if dist_phrase == None:
            assert omega != None
            self.infer_dist_phrase = True
            self.n_z_p = np.zeros((K, P)) + omega
            self.dist_z_p = np.array([np.random.dirichlet(omega)
                    for z in xrange(K)])

        for doc_meta in docs_meta:
            # assign initial topic label for each paper
            if smartinit:
                pass
            else:
                # z = np.random.randint(0, K)
                z = 0
                self.z_d[doc_meta.doc_id] = z

            # set initial counters
            self.n_z[z] += 1
            for a in doc_meta.authors:
                self.n_z_a[z][a] += 1
            self.n_z_v[z][doc_meta.venue] += 1
            if self.infer_dist_phrase:
                for (p, cnt) in doc_meta.phrases.items():
                    self.n_z_p[z][p] += cnt

    def infer(self):
        """learning once interation"""
        # sample topic label for each paper
        for doc_meta in self.docs_meta:
            # discount the current topic label
            z = self.z_d[doc_meta.doc_id]
            self.n_z[z] -= 1
            for a in doc_meta.authors:
                self.n_z_a[z][a] -= 1
            self.n_z_v[z][doc_meta.venue] -= 1

            if self.infer_dist_phrase:
                for (p, cnt) in doc_meta.phrases.items():
                    self.n_z_p[z][p] -= cnt

            # sample a new topic label
            p_z = np.empty(self.K)
            for z_i in xrange(self.K):
                p_z_i = self.n_z[z_i]
                for a in doc_meta.authors:
                    p_z_i *= self.dist_z_a[z_i][a]
                p_z_i *= self.dist_z_v[z_i][doc_meta.venue]
                for (p, n_i_p) in doc_meta.phrases.items():
                    p_z_i *= np.power(self.dist_z_p[z_i][p], n_i_p)
                p_z[z_i] = p_z_i
            new_z = np.random.multinomial(1, p_z / p_z.sum()).argmax()

            # print "old_z: ", z, "new_z: ", new_z
            # set the new topic label and increase the counters
            self.z_d[doc_meta.doc_id] = new_z
            self.n_z[new_z] += 1
            for a in doc_meta.authors:
                self.n_z_a[new_z][a] += 1
            self.n_z_v[new_z][doc_meta.venue] += 1
            if self.infer_dist_phrase:
                for (p, cnt) in doc_meta.phrases.items():
                    self.n_z_p[new_z][p] += cnt

        # sample new author and venue distributions for each topic
        self.dist_z_a = np.array([np.random.dirichlet(self.n_z_a[z])
                                 for z in xrange(self.K)])
        self.dist_z_v = np.array([np.random.dirichlet(self.n_z_v[z])
                                 for z in xrange(self.K)])
        if self.infer_dist_phrase:
            self.dist_z_p = \
                np.array([np.random.dirichlet(self.n_z_p[z]) for z in
                         xrange(self.K)])


def expert_finding_learning(expert_finder, iteration):
    for i in xrange(iteration):
        expert_finder.infer()
        print 'iter: ', i
        print 'topics: ', expert_finder.z_d
        print 'author: ', expert_finder.dist_z_a
        print 'venues: ', expert_finder.dist_z_v
        print '\n'


if __name__ == '__main__':
    alpha = np.ones(2)
    beta = np.ones(3)
    gamma = np.ones(2)
    omega = np.ones(5)
    doc1 = DocMeta(0, {0: 2, 1: 2, 4: 1}, [0, 1], 0)
    doc2 = DocMeta(1, {
        3: 2,
        4: 1,
        0: 1,
        2: 1,
        }, [1, 2], 1)
    dist_phrase = np.array([[0.4, 0.3, 0.2, 0.08, 0.02], [0.06, 0.03,
                           0.01, 0.5, 0.4]])
    test1 = ExpertFinder(
        2,
        [doc1, doc2],
        5,
        3,
        2,
        alpha,
        beta,
        gamma,
        None,
        dist_phrase,
        )
    test2 = ExpertFinder(
        2,
        [doc1, doc2],
        5,
        3,
        2,
        alpha,
        beta,
        gamma,
        omega,
        )
    expert_finding_learning(test1, 10)
