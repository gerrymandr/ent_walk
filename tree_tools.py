# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 13:40:29 2018

@author: MGGG
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 12:01:21 2018

@author: MGGG
"""

import networkx as nx
import numpy as np
import scipy.linalg
from scipy.sparse import csc_matrix
import scipy
from scipy import array, linalg, dot
from projection_tools import remove_edges_map

from networkx.algorithms.centrality.flow_matrix import *


######Tree counting

def log_number_trees(graph, weight = False):
    '''Computes the log of the number of trees, weighted or unweighted. 
    
    :graph: The input graph
    :weight: the edge variable name that describes the edge weights
    
    '''
    #Kirkoffs is the determinant of the minor..
    #at some point this should be replaced with a Cholesky decomposition based algorithm, which is supposedly faster. 
    if weight == False:
        m = nx.laplacian_matrix(graph)[1:,1:]
    if weight == True:
        m = nx.laplacian_matrix(graph, weight = "weight")[1:,1:]
    m = csc_matrix(m)
    splumatrix = scipy.sparse.linalg.splu(m)
    diag_L = np.diag(splumatrix.L.A)
    diag_U = np.diag(splumatrix.U.A)
    S_log_L = [np.log(np.abs(s)) for s in diag_L]
    S_log_U = [np.log(np.abs(s)) for s in diag_U]
    LU_prod = np.sum(S_log_U) + np.sum(S_log_L)
    return  LU_prod


def likelihood_tree_edges_pair(graph,tree,edge_list):
    '''
    
    This computes the partition associated ot (graph, tree, edge_list)
    and computes the log-likelihood that that partition is drawn via uniform tree
    with uniform edge_list sampling method
    
    graph = the graph to be partitioned
    tree = a chosen spanning tree on the graph
    edge_list = list of edges that determine the partition
    
    there are two terms in the log-likelihood:
        tree_term = from the number of spanning trees within each block
        connector_term = from the number of ways to pick a spanning tree to 
        hook up the blocks
    
    the way that connector_term works:
        1. It builds a graph whose nodes are the blocks in the partitions
        and whose multi-edges correspond to the set of edges connecting those blocks
        2. It uses the multi-graph (or weighted graph) version of Kirkoffs theorem to compute the
        ways to 
        
    the way that tree_term works:
        for each block of hte partition, it compute the number of spanning trees
        that that induced subgraph as.
    returns (tree term + connector term)
    TODO -- rewrite score to be 1 / this
    
    '''
    partition = remove_edges_map(graph, tree, edge_list)
    #this gets the list of subgraphs from (tree, edges) pair
    tree_term = np.sum([log_number_trees(g) for g in partition])

    #Building connector term:
    connector_graph = nx.Graph()
    connector_graph.add_nodes_from(partition)
    for subgraph_1 in partition:
        for subgraph_2 in partition:
            if subgraph_1 != subgraph_2:
                cutedges = cut_edges(graph, subgraph_1, subgraph_2)
                if cutedges != []:
                    connector_graph.add_edge(subgraph_1, subgraph_2, weight = len(cutedges))
    cut_weight = log_number_trees(connector_graph, True)
    return (tree_term + cut_weight)


def effective_resistance(graph, vertex_1, vertex_2, LU = 0):
    for vertex in graph.nodes():
            graph.nodes[vertex]["pos"] = vertex
    n= 10
    vertex_2 = 1
    vertex_1 = 2
    H = nx.relabel_nodes(graph, dict(zip(ordering, range(n))))
    L = laplacian_sparse_matrix(H, format='csc')
    solver = SuperLUInverseLaplacian(L, width=1) 
    return solver.get_row(vertex_2)[vertex_1]

    

       
###Emperical distribution creation tools
    
#To do: estimate the entropy of the TaTbcut(a,b) distribution

def count(x, visited_partitions):

    x_lens = np.sort([len(k) for k in x])
    count = 0
    for sample_nodes in visited_partitions:
        #sample_nodes = set([frozenset(g.nodes()) for g in i])
        sample_lens = np.sort([len(k) for k in sample_nodes])
        #if (x_lens == sample_lens).all():
        if np.array_equal(x_lens , sample_lens):
            if x == sample_nodes:
                count += 1
    return count


def make_histogram(A, visited_partitions):
    A_node_lists = [ set([frozenset(g.nodes()) for g in x]) for x in A]
    dictionary = {}
    for x in A_node_lists:
        dictionary[str(x)] = count(x,visited_partitions) / len(visited_partitions)
    return dictionary


def total_variation(distribution_1, distribution_2):
    total_variation = 0
    for k in distribution_1.keys():
        total_variation += np.abs(distribution_1[k] - distribution_2[k])
    return total_variation
##########################
 