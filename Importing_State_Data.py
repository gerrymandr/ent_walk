# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 10:39:18 2018

@author: MGGG
"""

from main import explore_random, total_pop

import json
import networkx as nx

state = "45"

with open("../vtd-adjacency-graphs/vtd-adjacency-graphs/"+str(state)+"/rook.json") as f:
    data = json.load(f)

graph = nx.readwrite.json_graph.adjacency_graph(data)

import glob
import pandas as pd

allFiles = glob.glob("../redistricting/adjacency_matrix_demo/spatial_indexes/"+str(state)+"_*_idx.txt")
frame = pd.DataFrame()
list_ = []
for file_ in allFiles:
    df = pd.read_csv(file_,index_col=None, header=None)
    list_.append(df)
frame = pd.concat(list_)

df = frame.rename(index=str, columns={0 : "GEOID", 1: "xaxis", 2:"yaxis"})
pos = df.set_index('GEOID').T.to_dict('list')
pos = {str(i) : (pos[i][0], pos[i][1]) for i in pos.keys()}

node_list = list(graph.nodes())
for node in node_list:
    try:
        graph.nodes[node]["geopos"] = pos[str(node)]
    except:
        exception = node
        print(node, type(node))
        print(graph.nodes[node])

import matplotlib.pyplot as plt
##
#plt.figure(figsize = (10,7))
#nx.draw(graph, pos = pos, node_size=0)
#
#print(len(graph))
#
#
parts = explore_random(graph, 1, 6, pictures = True, divide_and_conquer=False,with_walk = False, delta = .1)

#populations = [total_pop]