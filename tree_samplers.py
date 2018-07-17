# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 14:32:19 2018

@author: MGGG
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 11:43:31 2018

@author: MGGG
"""

#####For creating a spanning tree
import networkx as nx
import random
import math
from equi_partition_tools import equi_split, almost_equi_split, check_delta_equi_split
from projection_tools import remove_edges_map
from walk_tools import propose_step, propose_Broder_step
from Broder_Wilson_algorithms import random_spanning_tree_wilson, random_spanning_tree
#################
'''



'''

def random_partition(sampler):
                     
                     #graph, num_blocks, tree_algorithm, delta, pruning_algorithm):
    '''
        
    :graph:
    :num_partitions:
    :num_blocks: Number of blocks in each partition
    tree_algorithm = random_spanning_tree_wilson, random_spanning_tree_broder
    pruning_algorithm = almost_equi_split
    '''
    counter = 0
    while counter < 1000:
        counter += 1
        sampler.current_tree = sampler.tree_sampling_algorithm()
        sampler.edge_list = sampler.edge_selection_algorithm()
        if sampler.edge_list != None:
            blocks = sampler.remove_edges_map()
            print("waiting time:", counter)
            return blocks
        print("exceeded waiting time")
        return None
    
def tree_step(sampler):
    
    '''
    
    '''
    
def ent_walk(sampler):
    '''This takes sampler.current_pair, which is already a (T,E) tuple, does a walk on the (T,E) pairs (using sampler.walk_method)  
    sampler.tree = lift(sampler)
    '''
    
    
def instantiate_pair(partition)
    '''This takes the partition, and lifts it to a (T,E) tuple...
    '''
    
    
    
    
#def random_equi_partition_fast(graph, num_blocks, tree_algorithm, delta, pruning_algorithm):
#    '''This is a divide and conquer algorithm that speeds up the search
#    for an equipartition...
#    
#    The way it works is that it find a tree that equi-splits graph into two
#    subgraphs, and then repeats this procedure on each subgraph until we have 
#    the desired number of blocks in the subgraph.
#    
#    
#    '''
#    self.num_blocks = 2    
#    blocks = random_partition(graph, 2, tree_algorithm, delta, pruning_algorithm)
#    if blocks == None:
#        return None
#    while len(blocks) < 2**math.log(num_blocks, 2):
#        subgraph_splits = []
#        for subgraph in blocks:
#            if subgraph == None:
#                return None
#            self.working_subgraph = subgraph
#            subgraph_splits += self.random_partition()
#            #subgraph_splits += random_partition(subgraph, 2, tree_algorithm, delta, pruning_algorithm)
#        blocks = subgraph_splits
#    return blocks


############  Almost equi-partitions using sampling, then MH on trees 
    
    
'''To be filled in -- this will draw a random spanning tree, and check if it can be 
almost equi split (delta can be set to be zero...) 

[Aside: You can clean up the code by putting delta  =0 to be equi-partitions...]

then it will run a the tree walk, updated the labels dynamically, until it gets to a tree
that can be equi split...

'''

def random_almost_equi_partitions_with_walk(graph, num_partitions, num_blocks, delta, step = "Basis", jump_size = 50):
    '''This produces a delta almost equi partition... it keeps looping until it finds
    the required amounts
    
    '''
#    print("am here")
#    print(step)
    found_partitions = []
    counter = 0
    tree = random_spanning_tree_wilson(graph)
    while len(found_partitions) < num_partitions:
        counter += 1
        if step == "Basis":
            for i in range(jump_size):
                tree, edge_to_remove, edge_to_add = propose_step(graph, tree)
        if step == "Broder":
            for i in range(jump_size):
                tree, edge_to_remove, edge_to_add = propose_Broder_step(graph, tree)
        edge_list = almost_equi_split(tree, num_blocks, delta)
        #If the almost equi split was not a delta split, then it returns none...
        if edge_list != None:
            blocks = remove_edges_map(graph, tree, edge_list)
            found_partitions.append(blocks)
            print(len(found_partitions), "waiting time:", counter)
            counter = 0
    return found_partitions

##
def random_almost_equi_partition_fast_with_walk(graph, log2_num_blocks, delta, step, jump_size = 50):
    '''Divide and conquer approach to finding almost equi-partitions.
    Similar idea to random_equi_partition_fast
    
    '''
    blocks = random_almost_equi_partitions_with_walk(graph, 1, 2, delta, step, jump_size)[0]
    while len(blocks) < 2**log2_num_blocks:
        subgraph_splits = []
        for subgraph in blocks:
            subgraph_splits += random_almost_equi_partitions_with_walk(subgraph, 1, 2, delta, step, jump_size)[0]
        blocks = subgraph_splits
    return blocks

def random_almost_equi_partitions_fast_with_walk(graph, num_partitions, log2_num_blocks, delta, step = "Basis", jump_size = 50):
    '''This builds up almost-equi partitions, it called random_almost_equi_partitoins_fast
    which does a divide and consquer to build up partitions...
    
    '''
    found_partitions = []
    while len(found_partitions) < num_partitions:
        found_partitions.append(random_almost_equi_partition_fast_with_walk(graph, log2_num_blocks, delta, step, jump_size = 50))
    return found_partitions

