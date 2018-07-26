# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 12:04:47 2018

@author: MGGG
"""

'''This takes in (T,E) pair and updates it to return at (T',E) tuple...
note that E isn't necessarily a subset of the edegs of T'.'''

import random
import networkx as nx






#Below is copied over from tree w

def propose_step(graph,tree):
    '''
    this proposes a basis exchange move on the spanning trees
    definedin Broder //// also in /// (for matroid case)
    :graph: the ambient graph
    :tree: the current spanning tree
    
    Need to modify this so that it spits out a tree with appropriate directedness
    
    
    '''
    print("Propose step needs to be fixed! ... to include population")
    tree_edges = set(tree.edges())
    tree_edges_flipped = set([ tuple((edge[1], edge[0])) for edge in tree_edges])
    graph_edges = set(graph.edges())
    #tree is a digraph, so we need to check both possible orientatoins in order to add
    #an edge that makes an undirected cycle...
    
    
    edges_not_in_tree = list((graph_edges.difference(tree_edges)).difference(tree_edges_flipped))
    
    edge_to_add = random.choice(edges_not_in_tree)
    
    tree.add_edge(edge_to_add[0], edge_to_add[1])
    cycle = nx.find_cycle(tree, orientation = 'ignore')
    #Can this be sped up since we know that the cycle contains edge_to_add?
    
    edge_to_remove = random.choice(cycle)
    tree.remove_edge(edge_to_remove[0], edge_to_remove[1])
    
    
    
    
    re_rooted = nx.dfs_tree(tree.to_undirected(), list(tree.nodes())[0]).reverse()
    tree.graph["ordering"] = nx.topological_sort(tree)
    #This is still very inefficient! .reverse makes a whole new graph!
    
    #Want to make it so that we don't need to call dfs and reverse here...
    #Note clear how to do this... so instead, run Broders algorithm, which has
    #any easy update step...
    return re_rooted, edge_to_remove, edge_to_add

def propose_Broder_step(graph, tree):
    
    root = tree.graph["root"]
    new_root = random.choice(list(graph.neighbors(root)))
    remove_edge = list(tree.out_edges(new_root))[0]
    tree.add_edge(root, new_root)
    tree.remove_edge(remove_edge[0], remove_edge[1])
    tree.graph["root"] = new_root
    
    index_new_root = tree.graph["ordering"].index(new_root)
    tree.graph["ordering"].pop(index_new_root)
    tree.graph["ordering"].append(new_root)

    
    return tree, [remove_edge[0], remove_edge[1]], remove_edge
