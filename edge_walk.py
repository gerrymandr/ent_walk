# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 12:04:57 2018

@author: MGGG
"""

'''This takes in a (T',E) tuple, where E are not necessarily edges from T', and updates it to a (T',E'), where now E' are edges from T''''
import random
def uniformly_random(tree_edges_pair):
    new_edges = random.sample(list(tree_edges_pair.tree.edges()), tree_edges_pair.num_edges)
    tree_edges_pair.edges = new_edges
    