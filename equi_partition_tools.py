# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 11:42:30 2018

@author: MGGG
"""

''' Equipartition tools'''

import networkx as nx
import numpy as np
import random

def equi_split(tree, num_blocks):
    '''This will return a perfect equi-partition into num_blocks blocks
    It will do so by running choose best weight_hard to peel off pieces of 
    appropriate size
    
    this works because it is returning the edges, handling the components is done
    later...
    
    :tree:
    :num_blocks:
    '''
    label_weights(tree)
    found_edges = []
    found_blocks = 0
    while found_blocks < num_blocks - 1:
        edge = choose_best_weight_hard(tree, num_blocks)
        if edge != None:
            found_edges.append(edge)
            found_blocks += 1
            update_weights(tree, edge)
        if edge == None:
            return None
    return found_edges

def delta_equi_split(sampler):
    #(tree, num_blocks, delta):
    '''This returns a partition from the that is delta close to be an equi-partition
    
    Specifically, this runs choose_best_weight iteratively, which find an
    edge whose removal make a new partition of size closest to len(tree) / num_blocks
    
    :tree: the input tree
    :num_blocks: break tree in num_blocks partitions
    :delta: each block B must satisfy 1 - delta <= B / (tree / num_blocks) <= 1 + delta
    
    '''
    label_weights(sampler.tree)

    found_edges = []
    found_blocks = 0
    while found_blocks < sampler.num_blocks - 1:
        edge, ratio = choose_best_weight(sampler)
        if (ratio >= 1 + sampler.delta) or (ratio <= 1 - sampler.delta):
            return None
        found_edges.append(edge)
        found_blocks += 1
        update_weights(sampler.tree, edge)
    return found_edges 

#def check_delta_equi_split(subgraph_sizes, delta = .01):
#    '''returns True if all ratios of sizes are all within 1 + delta
#    :subgraph_sizes: list of sizes
#    '''
#
#    for i in range(len(subgraph_sizes)):
#        for j in range(i, len(subgraph_sizes)):
#            if subgraph_sizes[i]/subgraph_sizes[j] > 1 + delta:
#                return False
#    return True

def update_weights(tree, edge):
    '''update the weights of a graph after selecting an edge to cut
    this will set the weights above the edge to zero
    and below the edge will get decremented by 1
    '''
    
    head_node = edge[1]
    tail_node = edge[0]
    weight = tree.nodes[tail_node]["weight"] 
    set_label_zero_above(tree, tail_node)
    decrement_label_weights_below(tree, head_node, weight)

def set_label_zero_above(tree, node):
    '''sets the label weights to zero at and above node
    '''
       
    ordering = list(tree.graph["ordering"])

    tree.nodes[node]["weight"] = 0
    for node in ordering[::-1]:
        out_edge = list(tree.out_edges(node))
        if out_edge != []:
            if tree.nodes[out_edge[0][1]]["weight"] == 0:
                tree.nodes[node]["weight"] = 0
      
def test_tree(tree):
    '''For debugging purposes'''
    for vertex in tree:
            tree.nodes[vertex]["pos"] = vertex
    labels = nx.get_node_attributes(tree, "weight")
    nx.draw(tree, pos=nx.get_node_attributes(tree, 'pos'), labels= labels)

    
    
def decrement_label_weights_below(tree, start_node, weight):
    ''' Reduces the weight of all nodes at and below the start node'''
    
    node = start_node
    ordering = tree.graph["ordering"]

    for vertex in tree:
        tree.nodes[vertex]["touched"] = 0
    tree.nodes[node]["weight"] += -1 * weight
    tree.nodes[node]["touched"] = 1
    for node in ordering:
        in_edges = list(tree.in_edges(node))
        if in_edges != []:
            parents = [edge[0] for edge in in_edges]
            for parent in parents:
                if tree.nodes[parent]["touched"] == 1:
                    tree.nodes[node]["weight"] += -1 * weight
                    tree.nodes[node]["touched"] = 1
       
def label_weights(tree):
    '''
    Label nodes of of a directed, rooted tree by the weight above that node.
#
#    :tree: NetworkX DiGraph.
#    :returns: Nothing.
#
#    The "weight" of a node is the size of the subtree rooted at itself.
#    
#    TODO: implement a priority queue of weights so that you don't need to search through the graph...
    
    This is the nonrecursive version, which makes pyhton not crash...
    
    '''

    #This is a perfect problem for topological sorting!
    
    for node in tree.nodes:
        tree.nodes[node]["weight"] = tree.nodes[node]["POP10"]
    
    
    ordering = tree.graph["ordering"]

    for node in ordering:
        parents = [ edge[0] for edge in tree.in_edges(node)]
        for parent in parents:
            tree.nodes[node]["weight"] += tree.nodes[parent]["weight"]

    

def choose_best_weight_hard(tree, num_blocks):
    '''Returns an edge that cuts of a chunk of size n_nodes/ num_blocks
    if it exists. Otherwise returns None.
    
    :graph:
    :returns: edge
    '''
    size = len(tree.nodes()) / num_blocks
    for node in tree:
        if tree.nodes[node]["weight"] == size:
            return list(tree.edges(node))[0]
    return None

def choose_best_weight(tree, num_blocks):
    """Choose edge from graph with weight closest to n_nodes / num_blocks.

    :graph: NetworkX Graph labeled by :func:`~label_weights`.
    :returns: Tuple (edge, weight).

    """
    
    pop = [tree.nodes[i]["POP10"] for i in tree.nodes()]
    len_tree = np.sum(pop)
    ###This should be changed to total populatoin.
    
    ideal_value = len_tree/ num_blocks
    best_node = None
    best_difference = float("inf")
    tree_nodes = list( set(tree.nodes()).difference( set( tree.graph["root"])) )
    #Not allowed to pick root, causes problems
    random.shuffle(tree_nodes)
    for node in tree_nodes:
        diff = abs(ideal_value - tree.nodes[node]["weight"])
        if diff < best_difference:
            best_node = node
            best_difference = diff

    edge = list(tree.edges(best_node))[0]
    weight = tree.nodes[best_node]["weight"]

    return (edge, ideal_value /  weight)
