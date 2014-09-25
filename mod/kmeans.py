#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-09-12 09:29:12
# @Author  : yml_bright@163.com

import numpy as np
import random
 
def cluster_points(X, mu):
    clusters  = {}
    clu = {}
    for k in range(len(X)):
        bestmukey = min([(i[0], np.linalg.norm(X[k]-mu[i[0]])) \
                    for i in enumerate(mu)], key=lambda t:t[1])[0]
        try:
            clusters[bestmukey].append(X[k])
            clu[bestmukey].append(k)
        except KeyError:
            clusters[bestmukey] = [X[k]]
            clu[bestmukey] = [k]
    return clusters,clu
 
def reevaluate_centers(mu, clusters):
    newmu = []
    keys = sorted(clusters.keys())
    for k in keys:
        newmu.append(np.mean(clusters[k], axis = 0))
    return newmu
 
def has_converged(mu, oldmu):
    return (set([tuple(a) for a in mu]) == set([tuple(a) for a in oldmu]))
 
def find_centers(X, K):
    X = np.array(X)
    # Initialize to K random centers
    oldmu = np.array(random.sample(X, K))
    mu = np.array(random.sample(X, K))
    while not has_converged(mu, oldmu):
        oldmu = mu
        # Assign all points in X to clusters
        clusters,clu = cluster_points(X, mu)
        # Reevaluate centers
        mu = reevaluate_centers(oldmu, clusters)
    return(mu, clu)

if __name__ == '__main__':
    x = [[1],[1],[2],[3],[10],[12],[2],[13]]
    a,b = find_centers(x,5)
    print a
    print b