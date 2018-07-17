# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 17:32:53 2018

@author: MGGG
"""

from walk_tools import equi_shadow_walk
import networkx as nx
from tree_sampling_tools import random_equi_partitions, random_spanning_tree, random_spanning_tree_wilson, random_equi_partitions_fast, random_almost_equi_partitions_fast, random_almost_equi_partitions, random_almost_equi_partitions_with_walk, random_almost_equi_partitions_fast_with_walk
from equi_partition_tools import check_delta_equi_split
from visualization_tools import visualize_partition, visualize_partition_with_populations
import numpy as np


def explore_random(graph, num_maps, num_blocks, pictures = False, divide_and_conquer = False, equi = False, with_walk = True, delta = .1):
    '''This samples random equi-partitoins according to natural likelihood
    
    :fast: The divide and conquer strategy. Currently unclear what distirbution this gives.
    :pictures: whether to display pictures of the found plan
    :num_maps: number of maps to produce
    :num_blocks: number of blocks in each map
    :pictures: whether to display a picture at the end
    :divide_and_conquer: whether to use a divide and conquer algorithm... currently
    input muts by a power of 2
    :equi: Whether to hard constraint to same sized partitions
    :delta: the tolerance with which to accept partitions that are not equal sized.
     
    '''
    
    
    '''easy fixes:
        
        1. Replace equi with delta = 0
        2. 
        
    '''
    if with_walk == True:
        step = "Broder"
        jump_size = 1
        tree_partitions = random_almost_equi_partitions_with_walk(graph, 1, num_blocks, delta, step, jump_size)
    if with_walk == False:
     # Checking partition parameter selections
        if equi and divide_and_conquer:
            log2_num_blocks = np.log2(num_blocks)
            if int(log2_num_blocks) != log2_num_blocks:
                print("Must be power of 2 number of blocks")
                return
            tree_partitions = random_equi_partitions_fast(graph, num_maps, log2_num_blocks)
        elif equi and not divide_and_conquer:
            tree_partitions = random_equi_partitions(graph, num_maps, num_blocks)
        elif not equi and divide_and_conquer:
            log2_num_blocks = np.log2(num_blocks)
            if int(log2_num_blocks) != log2_num_blocks:
                print("Must be power of 2 number of blocks")
                return
            tree_partitions = random_almost_equi_partitions_fast(graph, num_maps, log2_num_blocks, delta)
        elif not equi and not divide_and_conquer:
            tree_partitions = random_almost_equi_partitions(graph, num_maps, num_blocks, delta)
    
    # Visualizations        
    if pictures == True:
        for partition in tree_partitions:
            visualize_partition(graph, partition)
            print("Node sizes", [len(x) for x in partition])
            print("Population", [total_pop(x) for x in partition])
            
    return tree_partitions

def total_pop(graph):
    
    return np.sum( [graph.nodes[x]["POP10"] for x in graph.nodes()] )


def explore_walk(graph_size, num_blocks):
    '''
    This does tree walk to sample equi-partitions
    '''
    graph = nx.grid_graph( [graph_size, graph_size])
    tree = random_spanning_tree(graph)
    tree_partitions =  equi_shadow_walk(graph, tree,  3, num_blocks)
    return tree_partitions

def test(graph_size, num_blocks, delta):
    graph = nx.grid_graph([graph_size, graph_size])
    tree_partitions = random_almost_equi_partitions_with_walk(graph, 1, num_blocks, delta)
    for partition in tree_partitions:
        visualize_partition(graph, partition)
        print([len(x) for x in partition])
        
def test_fast_with_walk(graph_size, num_blocks, delta, step = "Basis", jump_size = 50):
    graph = nx.grid_graph([graph_size, graph_size])
    for vertex in graph:
        graph.nodes[vertex]["geopos"] = vertex
        graph.nodes[vertex]["POP10"] = 1
    tree_partitions = random_almost_equi_partitions_fast_with_walk(graph, 1, num_blocks, delta, step, jump_size)
    for partition in tree_partitions:
        visualize_partition(graph, partition)
        print([len(x) for x in partition])
        
        
    
#graph = nx.grid_graph([50,50])
#tree_1 = random_spanning_tree(graph)
#tree_2 = random_spanning_tree_wilson(graph)    

#test_fast_with_walk(120, 2, 0.01, "Broder", 1000)

'''
Observations: 
    
    1. When doing divide and conquer with walk, you don't need ot redraw a new tree
at each stage, instead... just copy them over and have them start walking...
2. When updating with Broder walk, we should update the weights dynamically...
3. Another option is 

Start a Broder walk, and build a forward tree... then after you've covered a certain 
percentage of nodes, switch to Wilsons...

.... A compromise might be : sample a tree, and then do the Broder walk until you get an 
equi partitoin, or an almost equipartition...

'''

'''
TODO:
    
    1. Update labels dynamically --- for Broder walk anyway
    2. Try a mixture of Broder and Wilson for generating the original walk.
    3. NOTE -- If possible, I want to stick to a process which is guaranteed to sample uniformly form trees
    ... so doing the walk until we get a tree that can be equisplit is preferable...
    4. 
'''


'''
Propose step is so slow!! It shouldn't be this slow!

Also I'm calling label_weights much more often than I should be... we should update
then dynamically when doing the tree walk...

'''

#The efficiency of this can depend on a lot whether you land near somewhere thats an
#equipartition... maybe can be faster if we do the label updating in a smart way.

#parts = explore_random(40,1,2, pictures = True, divide_and_conquer = True, equi = False, graph_type = "grid", delta = .2)
#parts = explore_random(120,1,12, pictures = True, divide_and_conquer = False, equi = False, delta = .1)
#check_delta_equi_split([len(x) for x in parts[0]], .01)
#explore_walk(8,4)
#
#parts = explore_random(10,1,3, pictures = True, divide_and_conquer = False, equi = False, graph_type = "dodeca")

'''
Todo: intead of hard equi partitions, expand it to delta equi... and 
get all delta equi partitions... is this going to slow down the check step?

Add a score function -- 

1. Draw a random tree
2. Add node weights
3. Draw random edges until you get one that lives within delta of ok (hard or soft...)
4. Accept it.

"Turtles on turtles..." but may work well.

'''

    
    