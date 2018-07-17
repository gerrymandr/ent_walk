# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 11:44:50 2018

@author: MGGG
"""

from equi_partition_tools import equi_split
import itertools
import networkx as nx
import random

######Projection tools:
    
    
def remove_edges_map(graph,tree,edge_list):
    '''This is the map that produces a partition from a tree and a list of edges
    
    :graph: the graph to be partitioned
    :tree: a chosen spanning tree on the graph
    :edge_list: a list of edges of the tree
    
    returns list of subgraphs induced by the components of the forest
    obtained by removing 'edge_list edges from  tree
    
    these correspond to the 'districts'

    '''
    tree.remove_edges_from(edge_list)
    components = list(nx.connected_components(tree.to_undirected()))
    tree.add_edges_from(edge_list)
    subgraphs = [nx.induced_subgraph(graph, subtree) for subtree in components]
    #This is expensive - TODO in case of error
    return subgraphs


def random_lift(graph, subgraphs):
    '''
    
    '''
    print("You haven't fixed this to be directed...")
    number_of_parts = len(subgraphs)
    subgraph_trees = [random_spanning_tree(g) for g in subgraphs]
    
    #This builds a graph with nodes the subgraph, and they are connected
    #if there is an edge connecting the two subgraphs
    #and each edge gets 'choices' = to all the edges in G that connect the two subgraphs
    connector_graph = nx.Graph()
    connector_graph.add_nodes_from(subgraphs)
    for subgraph_1 in subgraphs:
        for subgraph_2 in subgraphs:
            if subgraph_1 != subgraph_2:
                cutedges = cut_edges(graph, subgraph_1, subgraph_2)
                if cutedges != []:
                    connector_graph.add_edge(subgraph_1, subgraph_2, choices = cutedges)
                    #need to worry about directendess!!???
                    
                    
    connector_meta_tree = random_spanning_tree(connector_graph)
    connector_tree = nx.Graph()
    for e in connector_meta_tree.edges():
        w = random.choice(connector_graph[e[0]][e[1]]['choices'])
        connector_tree.add_edges_from([w])
        
    
    tree = nx.Graph()
    for sub_tree in subgraph_trees:
        tree.add_edges_from(sub_tree.edges())
    tree.add_edges_from(connector_tree.edges())
    edge_list = random.sample(list(T.edges()),number_of_parts - 1)
    return [tree, edge_list]

#####For lifting:

def cut_edges(graph, subgraph_1, subgraph_2):
    '''Finds the edges in graph from 
    subgraph_1 to subgraph_2
    
    :graph: The ambient graph
    :subgraph_1: 
    :subgraph_2:
        

    '''
    edges_of_graph = list(graph.edges())

    list_of_cut_edges = []
    for e in edges_of_graph:
        if e[0] in subgraph_1 and e[1] in subgraph_2:
            list_of_cut_edges.append(e)
        if e[0] in subgraph_2 and e[1] in subgraph_1:
            list_of_cut_edges.append(e)
    return list_of_cut_edges