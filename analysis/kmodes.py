# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 11:26:23 2023

@author: Ann
"""

import pandas as pd

from kmodes.kmodes import KModes
import matplotlib.pyplot as plt


#  %matplotlib inline


params = pd.read_csv('data/GameParams.csv',
                   dtype={'name': str},
                   header=0,
                   index_col='name')

# %%

def find_n_clusts(data):

    # Elbow curve to find optimal K
    cost = []
    K = range(1,40)
    for k in K:
        kmode = KModes(n_clusters=k, init="random", n_init=5, verbose=1)
        kmode.fit_predict(data)
        cost.append(kmode.cost_)

    plt.plot(K, cost, 'x-')
    plt.xlabel('No. of clusters')
    plt.ylabel('Cost')
    plt.title('Elbow Curve')
    plt.show()


# %%

def do_cluster(data, nclusters):

    kmode = KModes(n_clusters=nclusters, init="random", n_init=5, verbose=1)
    assigns = kmode.fit_predict(data)

    clusts = [[] for _ in range(nclusters)]
    for name, clust in zip(data.index, assigns):
        clusts[clust] += [name]

    return clusts

# %%


 #  this is not deterministic

find_n_clusts(params)

do_cluster(params, 12)

# %%
sel_cols = ['child_type', 'crosscapt', 'goal', 'mlaps', 'no_sides',
            'rounds', 'sow_own_store', 'udirect']
selected = params[sel_cols]

find_n_clusts(selected)


for cl in do_cluster(selected, 12):
    print(cl)
