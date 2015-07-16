#!/usr/bin/python
# -*- coding: utf-8 -*-

# ExpertFinder + collapsed Gibbs sampling
# Author: Hao Luo

import os

import numpy as np

from doc_meta import DocMeta
import file_io as fio

class ExpertFinder(object):

    def __init__(self, K, docs_meta, P, A, V,
    	alpha, beta, gamma, omega=None,
        dist_phrase=None,smartinit=False,
        init_from_file=False,
        n_z=None, n_z_a=None, n_z_v=None,
        z_d=None, 
        dist_z_a=None, dist_z_v=None, dist_z_p=None,
        ):
        self.K = K
        self.alpha = alpha  # hyperparameter for topics prior
        self.beta = beta  # hyperparameter for authors prior
        self.gamma = gamma  # hyperparameter for venues prior
        self.omega = omega
        self.dist_phrase = dist_phrase
        self.docs_meta = docs_meta
        self.P = P
        self.A = A
        self.V = V

        if init_from_file:
            self.n_z, self.n_z_a, self.n_z_v = n_z, n_z_a, n_z_v
            self.z_d = z_d
            self.dist_z_a, self.dist_z_v, self.dist_z_p = dist_z_a, dist_z_v, dist_z_p
        else:
            self.init_dist(smartinit)

    def init_dist(self, smartinit):
        self.n_z = np.zeros(self.K) + self.alpha  # paper count for each topic
        self.n_z_a = np.zeros((self.K, self.A)) + self.beta  # paper count for each topic and author
        self.n_z_v = np.zeros((self.K, self.V)) + self.gamma  # paper count for each topic and venue
        self.z_d = np.empty(len(self.docs_meta))  # topic for each paper

        self.dist_z_a = np.array([np.random.dirichlet(self.beta) for z in
                                 xrange(self.K)])
        self.dist_z_v = np.array([np.random.dirichlet(self.gamma[z]) for z in
                                 xrange(self.K)])

        self.dist_z_p = self.dist_phrase
        self.infer_dist_phrase = False
        if self.dist_phrase == None:
            assert self.omega != None
            self.infer_dist_phrase = True
            self.n_z_p = np.zeros((self.K, self.P)) + self.omega
            self.dist_z_p = np.array([np.random.dirichlet(self.omega[z])
                    for z in xrange(self.K)])

        for doc_meta in self.docs_meta:
            # assign initial topic label for each paper
            if smartinit:
                pass
            else:
                z = np.random.randint(0, self.K)
                #z = 0
                self.z_d[doc_meta.doc_id] = z

            # set initial counters
            self.n_z[z] += 1
            for a in doc_meta.authors:
                self.n_z_a[z][a] += 1
            self.n_z_v[z][doc_meta.venue] += 1
            if self.infer_dist_phrase:
                for (p, cnt) in doc_meta.phrases.items():
                    self.n_z_p[z][p] += cnt

    def save(self, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        np.save(output_dir + 'alpha', self.alpha)
        np.save(output_dir + 'beta', self.beta)
        np.save(output_dir + 'gamma', self.gamma)
        if self.omega != None:
            np.save(output_dir + 'omega', self.omega)
        np.save(output_dir + 'n_z', self.n_z)
        np.save(output_dir + 'n_z_a', self.n_z_a)
        np.save(output_dir + 'n_z_v', self.n_z_v)
        #np.save(output_dir + 'n_z_p', self.n_z_p)
        np.save(output_dir + 'z_d', self.z_d)
        np.save(output_dir + 'dist_z_a', self.dist_z_a)
        np.save(output_dir + 'dist_z_v', self.dist_z_v)
        np.save(output_dir + 'dist_z_p', self.dist_z_p)

    @classmethod  #TODO: currently does not support reconstruct doc-meta, thus could not infer after loading
    def load(cls, output_dir):
        alpha = np.load(output_dir + 'alpha.npy')
        beta = np.load(output_dir + 'beta.npy') 
        gamma = np.load(output_dir + 'gamma.npy')
        omega = None  #TODO: check if "output_dir + omega" exists: if yes load it; no, assign None
        n_z = np.load(output_dir + 'n_z.npy')
        n_z_a = np.load(output_dir + 'n_z_a.npy')
        n_z_v = np.load(output_dir + 'n_z_v.npy')
        #n_z_p = np.load(output_dir + 'n_z_p')
        z_d = np.load(output_dir + 'z_d.npy')
        dist_z_a = np.load(output_dir + 'dist_z_a.npy')
        dist_z_v = np.load(output_dir + 'dist_z_v.npy')
        dist_z_p = np.load(output_dir + 'dist_z_p.npy')
        K, P, A, V = n_z.shape[0], dist_z_p.shape[1], n_z_a.shape[1], n_z_v.shape[1]

        cls = ExpertFinder(
            K=K,
            docs_meta = None, #TODO = =
            P=P, A=A, V=V,
            alpha=alpha, beta=beta, gamma=gamma, omega=omega,
            dist_phrase=None,
            smartinit=False,
            init_from_file=True,
            n_z=n_z, n_z_a=n_z_a, n_z_v=n_z_v,
            z_d=z_d,
            dist_z_a=dist_z_a, dist_z_v=dist_z_v, dist_z_p=dist_z_p,
            )
        return cls
            
            
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
        print 'iter: ', i
        fio.log_ranking(expert_finder.dist_z_a, 'author', i)
        fio.log_ranking(expert_finder.dist_z_v, 'venue', i, topn=23)
        expert_finder.infer()
