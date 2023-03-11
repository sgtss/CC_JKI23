# %% 
#!/usr/bin/env python

# %% [markdown]

# **Challenge One - Basic algorithms**
#
# Importing numpy to hold adjancy matrix as nxn dense array and converting into sparse matrix in Compressed Sparse Row format of SciPy.
# For large graphs, use adjacency_list, edge_list or graphml. Or import and process dataframe from t/csv using pandas.
# For pre-existing datasets, try NetSet and Konect.

# %%
# Importing argparse to check args and file
import sys, argparse

import numpy as np
from numpy import genfromtxt
from scipy import sparse
#import pandas as pd

# Importing sknetwork library and components (Class/functions) to process DAG.
import sknetwork as skn
#from sknetwork.data import from_edge_list, from_adjacency_list, from_graphml, from_csv
from sknetwork.utils.check import is_symmetric
from sknetwork.topology import is_acyclic
from sknetwork.path import get_shortest_path

# Importing sknetwork and IPython libraries for visualization.
#from sknetwork.visualization import svg_graph
#from IPython.display import SVG

# %%
# Initializing default input parametersy
adj_matrix_array = None     # Provided DAG matrix
src_node = 5                # Root/source node of DAG matrix
tgt_node = 0                # Target node of DAG matrix

# process invocation cmd args
def getArgs():

    # Stores text for instructions
    INFO_ARG1 = "path to TAB/Comma seperated file with Adjacency matrix, for eg. data/sample1.tsv"
    INFO_ARG2 = "Root/Source node of Adjacency matrix"
    INFO_ARG3 = "Destination/target node of Adjacency matrix"

    # Parse arguments and validate
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='input_file', help=INFO_ARG1, type=argparse.FileType('r', encoding='utf-8'), metavar='Input', required=True)
    parser.add_argument('-s', dest='input_src_node', type=int, help=INFO_ARG2, metavar='Source', required=True)
    parser.add_argument('-t', dest='input_tgt_node', type=int, help=INFO_ARG3, metavar='Target', required=True)
    #args = parser.parse_args()
    return parser.parse_args()

args = getArgs()

#print(args.input_file)

# Updating input arguments
adj_matrix_array = genfromtxt(args.input_file, delimiter=',')
src_node = args.input_src_node
tgt_node = args.input_tgt_node

#print(adj_matrix_array)
#print(adj_matrix_array.shape)
#print(type(adj_matrix_array))

# Intial checks to determine if adjacent matrix of DAG contains weighted edges
# Negative cycles can lead to aberant results with Dijkstra’s algorithm

# Store number of Positive/Negative weights of given adj_matrix_array 
num_of_pos_weights_not_ones = np.count_nonzero((adj_matrix_array > 0) & (adj_matrix_array != 1))    # adjacent matrix of DAG containing positive weights other than ones must be weighted
num_of_pos_weights = np.count_nonzero(adj_matrix_array > 0)                                         # positive weights in adjacent matrix of undirected graph represent edges
num_of_neg_weights = np.count_nonzero(adj_matrix_array < 0)                                         # adjacent matrix containing negative weights must be weighted

#print("Num of Neg Wts: ", num_of_neg_weights)
#print("Num of Pos Wts (inc 1s): ", num_of_pos_weights)
#print("Num of Pos Wts (exc 1s): ", num_of_pos_weights_not_ones)

# convert nxn array to sparse matrix in CSR formmat
adj_mat_sparse_csr = sparse.csr_matrix(adj_matrix_array)                                            # especially efficient with large data sets

#print(adj_mat_sparse_csr)
#print(adj_mat_sparse_csr.shape)

# Generate svg graphics to check correctness 
#image = svg_graph(adj_mat_sparse_csr)
#SVG(image)

# %% [markdown]
#**TASK ONE:**
# Testing if provided DAG (adjancy matrix) is :
# 1) directed
# 2) acyclic
# 3) weighted and/or contains -ve weights

# %%
# setting up booleans to be used later to select best performing algorithms
directed = False if is_symmetric(adj_mat_sparse_csr) else True      # Symmmetric adjacent matrix must be undirected
acyclic = is_acyclic(adj_mat_sparse_csr)                            # adjacent matrix diagonal containing only zeros muust have no cycles
weighted_edges = True if (num_of_pos_weights_not_ones > 0) or (num_of_neg_weights > 0) else False
neg_weighted_edges = True if (num_of_neg_weights > 0) else False

#print("directed: ", directed)
#print("acyclic: ", acyclic)
#print("weighted: ", weighted_edges)

# %% [markdown]
#**TASK TWO:**

# Estimating depth (number of edges from given root) of given node.
# Step 1: Select best suited algorithm based on directness, cyclicity and weight of edges.
# Step 2: Find shortest path fron node [n] to root [r].
# Step 3: Count number of edges in the shortest path.
# 
# %% 
# Function to return depth of given node [n: tgt_node] to root node [r: source node] in given DAG as adjency matrix [dag_adj_matrix]
# However, adjency matrix [dag_adj_matrix] is converted into sparse matrix earlier [adj_mat_sparse_csr] and this function actually uses it
# suitable algorithm is selected based on above defined characteristics of above adjency matrix
# now works with non-DAG matrices as well
def GetDepthOfDAG():

    # intitalizing with none, value is updated based on characteristcs 
    # BF: Bellman-Ford, D: Dijkstra’s with Fibonacci heaps, FW: Floyd-Warshall and J: Johnson’s algorithm
    algorithm='none'  

    # if/else loop checking characteristics
    if directed:                    # is directed graph
        if acyclic:                 # is directed acylic graph
            if neg_weighted_edges:
                print('\nThe provided graph is Directed Acyclic Graph (DAG) with negative weighted edges.\nEvaluating using Johnson\'s algorithm:\n')
                algorithm='J'       # is neg-weighted dag; dont use D
            elif weighted_edges:
                print('\nThe provided graph is Directed Acyclic Graph (DAG) with weighted edges.\nEvaluating using Johnson\'s algorithm:\n')
                algorithm='J'       # is weighted dag; neg weights would have been caught above, can use D, but J appears to be faster
            else:
                print('\nThe provided graph is Directed Acyclic Graph (DAG).\nThe edges appear to be un-weighted.\nEvaluating using Dijkstra\'s algorithm:\n')
                algorithm='D'       # is un-weighted dag; can use D, but J appears to be faster
        elif not acyclic:           # detected pos/neg cycles in graph
            if neg_weighted_edges:
                print('\nThe provided graph is Directed Graph (DG) with cyclic nodes and negative weighted edges.\nEvaluating using Johnson\'s algorithm:\n')
                algorithm='J'       # is neg-weighted dcg; dont use D, may raise neg-cycle error, J is safer
            elif weighted_edges:
                print('\nThe provided graph is Directed Graph (DG) with cyclic nodes and weighted edges.\nEvaluating using Johnson\'s algorithm:\n')
                algorithm='J'       # is weighted dcg;  J appears to be consistent and faster
            else:
                print('\nThe provided graph is Directed Graph (DG) with cyclic nodes and un-weighted edges.\nEvaluating using Johnson\'s algorithm:\n')
                algorithm='J'       # is un-weighted dcg; self cycles may pop up, use J to be safe
        else:
            print('\nThe cyclicity and weight of nodes and edges can not be determined of this provided Directed Graph (DG).\nEvaluating using Johnson\'s algorithm:\n')
            algorithm='J'           # may be multi-graph or typos or formatting errors; use J to be safe
    elif not directed:              # is un-directed graph
        if acyclic:                 # no cycles detected
            print('\nThe provided graph is an UN-Directed Graph (UDG) with acyclic nodes and un-weighted edges.\nEvaluating using Johnson\'s algorithm:\n')
            algorithm='J'           # J and BF can be used, FW is too slow
        elif not acyclic:
            print('\nThe provided graph is an UN-Directed Graph (UDG) with cyclic nodes and un-weighted edges.\nEvaluating using Johnson\'s algorithm:\n')
            algorithm='J'           # J appears to be better
        else:
            print('\nThe cyclicity and weight of nodes and edges can not be determined of this provided Un-Directed Graph (DG).\n')
            algorithm='J'           # again J appears to be faster
    else:
        print('\nHouston, we have a problem!\n')    # maybe something went wrong in capturing adjency matrix

    # If capturing adjency matrix went ok
    if algorithm != 'none' and len(adj_matrix_array) > 0:

        # Find shortest path using sknetwork built-in function
        # based on SciPy (scipy.sparse.csgraph.shortest_path) 
        shortest_path = get_shortest_path(adj_mat_sparse_csr, method=algorithm, sources=src_node, targets=tgt_node)
        print('The shortest path between', src_node, 'and', tgt_node, 'is', shortest_path)
        print('The depth of target node [',tgt_node,'] is', len(shortest_path), '\n')

    else:
        print('\nThe characterization of provided graph failed.\nExiting script\n')

    return

GetDepthOfDAG()