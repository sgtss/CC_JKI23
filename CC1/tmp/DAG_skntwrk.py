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
from sknetwork.visualization import svg_graph

# Importing sknetwork library to process DAG.
from IPython.display import SVG

# %% [markdown]

# Setting up core functionality

# %%
# Test adjacency matrix; as 2D np_array
adj_matrix_array = np.array([[0, 1, 1, 0], [1, 0, 1, 1], [1, 1, 0, 0], [0, 1, 0, 0]]) # undirected; acyclic; unweigted
print(adj_matrix_array)

# Root/source node of DAG matrix
src_node = None

# Target node of DAG matrix
tgt_node = None

# convert nxn array to sparse matrix in CSR formmat
adj_mat_sparse_csr = sparse.csr_matrix(adj_matrix_array)
print(adj_mat_sparse_csr)

# Generate svg graphics to check correctness 
#image = svg_graph(adj_mat_sparse_csr)
#SVG(image)

# %% [markdown]
#**TASK ONE:**
# Testing if provided DAG (adjancy matrix) is :
# 1) directed
# 2) acyclic
# 3) weighted and/or contains -ve weights
