# %% 
#!/usr/bin/env python

# %% [markdown]

# **Challenge One - Basic algorithms**
#
# Importing numpy to hold adjancy matrix as nxn dense array and convert into sparse matrix in Compressed Sparse Row format of SciPy.
# For large graphs, use adjacency_list, edge_list or graphml. Or import and process dataframe from t/csv using pandas.
# For pre-existing datasets, try NetSet and Konect.

# %%
import numpy as np
from scipy import sparse
#import pandas as pd

# Importing sknetwork library and components (Class/functions) to process DAG.
import sknetwork as skn
#from sknetwork.data import from_edge_list, from_adjacency_list, from_graphml, from_csv
from sknetwork.utils.check import is_symmetric
from sknetwork.topology import is_acyclic


# Importing sknetwork and IPython libraries for visualization.
from sknetwork.visualization import svg_graph
from IPython.display import SVG

# %% [markdown]

# Setting up core functionality

# %%
# Provided DAG matrix
dag_adj_matrix = None

# Root/source node of DAG matrix
src_node = None

# Target node of DAG matrix
tgt_node = None

# Test adjacency matrix(s); as 2D np_array
#adj_matrix_array = np.array([[0,1,1,1,0,0], [1,1,0,0,1,0], [1,0,0,1,0,0], [1,0,1,0,1,1], [0,1,0,1,0,0], [0,0,0,1,0,1]]) # undirected; cyclic; un-weigted

#adj_matrix_array = np.array([[0,0,0,1,0,0], [1,1,0,0,0,0], [1,0,0,0,0,0], [0,0,1,0,1,0], [0,1,0,0,0,0], [0,0,0,1,0,1]]) # directed; cyclic; un-weigted
#adj_matrix_array = np.array([[0,0,0,0.4,0,0], [0.1,0.5,0,0,0,0], [0.9,0,0,0,0,0], [0,0,1.0,0,1.0,0], [0,0.5,0,0,0,0], [0,0,0,0.6,0,1.0]]) # directed; cyclic; pos-weigted
#adj_matrix_array = np.array([[0,0,0,-0.4,0,0], [0.1,0.5,0,0,0,0], [0.9,0,0,0,0,0], [0,0,1.0,0,1.0,0], [0,0.5,0,0,0,0], [0,0,0,0.6,0,1.0]]) # directed; cyclic; weigted (neg)

#adj_matrix_array = np.array([[0,0,0,0,0,0], [1,0,0,0,0,0], [0,1,0,0,0,0], [0,0,1,0,0,0], [0,0,1,1,0,0], [0,0,0,0,1,0]]) # directed; acyclic; un-weigted
#adj_matrix_array = np.array([[0,0,0,0,0,0], [0.9,0,0,0,0,0], [0,0.5,0,0,0,0], [0,0,1,0,0,0], [0,0,1,0.9,0,0], [0,0,0,0,0.2,0]]) # directed; acyclic; pos-weigted
adj_matrix_array = np.array([[0,0,0,0,0,0], [0.9,0,0,0,0,0], [0,-0.5,0,0,0,0], [0,0,1,0,0,0], [0,0,1,0.9,0,0], [0,0,0,0,-0.9,0]]) # directed; acyclic; neg-weigted

#print(adj_matrix_array)
#print(adj_matrix_array.shape)

# Store number of Positive/Negative weights of given adj_matrix_array 
num_of_pos_weights_not_ones = np.count_nonzero((adj_matrix_array > 0) & (adj_matrix_array != 1))    # adjacent matrix of DAG containing positive weights other than ones must be weighted
num_of_pos_weights = np.count_nonzero(adj_matrix_array > 0)                                         # positive weights in adjacent matrix of undirected graph represent edges
num_of_neg_weights = np.count_nonzero(adj_matrix_array < 0)                                         # adjacent matrix containing negative weights must be weighted

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

directed = False if is_symmetric(adj_mat_sparse_csr) else True      # Symmmetric adjacent matrix must be undirected
acyclic = is_acyclic(adj_mat_sparse_csr)                            # adjacent matrix diagonal containing only zeros muust have no cycles
weighted = True if (num_of_pos_weights_not_ones > 0) or (num_of_neg_weights > 0) else False

print("Num of Neg Ws: ", num_of_neg_weights)
print("Num of Pos Ws (inc 1s): ", num_of_pos_weights)
print("Num of Pos Ws (exc 1s): ", num_of_pos_weights_not_ones)
print("directed: ", directed)
print("acyclic: ", acyclic)
print("weighted: ", weighted)
