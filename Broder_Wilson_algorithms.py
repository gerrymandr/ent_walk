# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 01:08:09 2018

@author: MGGG
"""
import random
import networkx as nx

'''

Broder's algorithm

'''
def simple_random_walk(graph,node):
    '''takes'''
    wet = set([node])
    trip = [node]
    graph_size = len(graph.nodes())
    while len(wet) < graph_size:
        next_step = random.choice(list(graph.neighbors(node)))
        wet.add(next_step)
        trip.append(next_step)
        node = next_step
    return trip

def forward_tree(graph,node):
    
    walk = simple_random_walk(graph, node)
    edges = []
    for vertex in graph.nodes():
        if (vertex != walk[0]):
            first_occurance = walk.index(vertex)
            edges.append( [walk[first_occurance], walk[first_occurance-1]])
    return edges

def random_spanning_tree(graph):
    #It's going to be faster to use the David Wilson algorithm here instead.
    tree_edges = forward_tree(graph, random.choice(list(graph.nodes())))
    tree = nx.DiGraph()
    for node in graph.nodes:
        node_attributes = list(graph.nodes[node].keys())
        tree.add_node(node)
        for attr in node_attributes:
            tree.nodes[node][attr] = graph.nodes[node][attr]

    tree.add_edges_from(tree_edges)
    return tree

##############
    
'''Wilsons Algorithm'''

def random_spanning_tree_wilson(graph):
    #The David Wilson random spanning tree algorithm
    tree_edges = []
    root = random.choice(list(graph.nodes()))
    hitting_set = set ( [ root])
    allowable_set = set(graph.nodes()).difference(hitting_set)
    len_graph = len(graph)
    len_hitting_set = 1
    while len_hitting_set < len_graph:
        #allowable_set = list(set(graph.nodes()).difference(hitting_set))
        #If we can handle the step of choosing the allowable set more 
        #efficiently, we can speed stuff up... this is the bottle neck
        start_node = random.choice(list(allowable_set))
        trip = random_walk_until_hit(graph, start_node, hitting_set)
        new_branch, branch_length = loop_erasure(trip)
        for i in range(branch_length - 1):
            tree_edges.append( [ new_branch[i], new_branch[i + 1]])
        for v in new_branch[:-1]:
            hitting_set.add(v)
            len_hitting_set += 1
            allowable_set.remove(v)
    tree = nx.DiGraph()
    # Adding nodes that inherit the attributes from the original graph
    
    
    for node in graph.nodes:
        node_attributes = list(graph.nodes[node].keys())
        tree.add_node(node)
        for attr in node_attributes:
            tree.nodes[node][attr] = graph.nodes[node][attr]
    tree.add_edges_from(tree_edges)
    tree.graph["root"] = root
    tree.graph["ordering"] = list(nx.topological_sort(tree))
    return tree

def random_walk_until_hit(graph, start_node, hitting_set):
    '''Does a random walk from start_node until it hits the hitting_set
    
    :graph: input graph
    :start_node: the node taht the graph starts at
    :hitting_set: the set to stop at, i.e. the tree we are building up
    
    '''
    
    current_node = start_node
    trip = [current_node]
    while current_node not in hitting_set:
        #Add weights here:
        current_node = random.choice(list(graph.neighbors(current_node)))
        
        ###
        trip.append(current_node)
    return trip

def loop_erasure(trip):
    '''erases loops from a trip
    
    :trip: input of node names...
    '''
    n = len(trip)
    loop_erased_walk_indices = []
    last_occurance = n - trip[::-1].index(trip[0]) - 1
    loop_erased_walk_indices.append(last_occurance)
    branch_length = 0
    while trip[loop_erased_walk_indices[-1]] != trip[-1]:
        last_occurance = n -  trip[::-1].index(trip[loop_erased_walk_indices[-1]])  -1
        loop_erased_walk_indices.append(last_occurance + 1)
        branch_length += 1
    loop_erased_trip = [trip[i] for i in loop_erased_walk_indices]
    
    return (loop_erased_trip, branch_length + 1)
    #I don't think that passing the length sped it up at all...?

############Non Uniform Spanning Tree Generation:
    
def random_greedy(graph):
    '''This uses prims algorithm with a random weighting to make a tree. 
    This is  slow.
    
    '''
    graph_edges = list(graph.edges())
    random.shuffle(graph_edges)
    tree = nx.Graph()
    for edge in graph_edges:
        tree.add_edge(edge[0], edge[1])
        if not nx.is_forest(tree):
            tree.remove_edge(edge[0], edge[1])
    return tree

