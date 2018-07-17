# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 17:28:34 2018

@author: MGGG
"""
from equi_partition_tools import equi_split
import random
import networkx as nx
from Broder_Wilson_algorithms import random_spanning_tree_wilson
from projection_tools import remove_edges_map
###Tree walk
    
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

def equi_shadow_step(graph, tree, num_blocks):
    '''
    Keeps walking on trees from current tree until it reaches a new tree that 
    has an equipartition
    
    :graph: the ambient graph
    :tree: the current tree
    :num_blocks: number of blocks
    '''
    
    while True:
        new_tree, edge_to_remove, edge_to_add = propose_step(graph, tree)
        edges = equi_split(new_tree, num_blocks)
        if edges != None:
            return (new_tree, edges)
        
def equi_shadow_walk(graph, tree, num_steps, num_blocks):
    found_partitions = []
    counter = 0
    while len(found_partitions) < num_steps:
        counter += 1
        tree, edge_list = equi_shadow_step(graph, tree, num_blocks)
        if edge_list != None:
            found_partitions.append( remove_edges_map(graph, tree, edge_list))
            print(len(found_partitions), "waiting time:", counter)
            counter = 0
    return found_partitions
        
def test():
    graph = nx.grid_graph([10,10])
    tree = random_spanning_tree(graph)
    equi_shadow_walk(graph, tree, 2)
    
#    
#def shadow_walk(graph, tree,e, equi_partition = False, metropolis = False):
#    '''
#    Proposes a tree walk step, and does MH
#    
#    '''
#    n = len(e)
#    U = propose_step(G,T)
#    if equi_partition == False:
#        e2 = random.sample(list(U.edges()),n)
#    if equi == True:
#        e2 = equi_split(G,T, n)
#    if MH == True:
#        current_score = 1 / likelihood_tree_edges_pair(G,T,e)
#        new_score = 1 / likelihood_tree_edges_pair(G, U, e2)
#        if new_score > current_score:
#            return [U,e2]
#        else:
#           p = np.exp(new_score - current_score)
#           a = np.random.uniform(0,1)
#           if a < p:
#               return [U,e2]
#           else:
#               return [T,e]
#    if MH == False:
#        return [U,e2]
#
