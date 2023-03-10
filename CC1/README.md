# **Challenge One - Basic algorithms**

**TASK ONE: Completed** 
Assume a directed acyclic graph (DAG) in which nodes can have multiple parents and there is a
single unique root node. The minimum number of edges connecting any node n with the DAG's
root node r is considered the depth d ( n ) of node n . Because a node can have many parents,
there might be several routes, of varying number of edges, from the node to the root r . Provide a
test (see Test Driven Development ) that executes your solution and verifies it works as
expected. 

**TASK TWO: Completed** 
Then write the function that returns the depth of a node given the DAG and test it with
your test. Assume the DAG, i.e. the input to your function, to be represented as an adjacency
matrix . Further input arguments are the node of interest, for which we want to know its depth,
and the root node, meaning that the root node is known so that your algorithm does not need to
find it. Use any programming language you like to solve this challenge. 

**TASK THREE: Completed**
You will receive extra points if you name at least two of the three standard algorithms that solve this challenge - or the
other one(s) apart from the algorithm you applied in your solution.

**TASK FOUR: Not Attempted**
Alternatively, you can receive extra points if you implement the solution in either Brainfuck or
Assembler , but because you will be considered not totally sane we will not invite you to dinner.

**SOLUTIONS:**
Please see results folder.

*USAGE: python code/DAG_analysis_sknetwork.py -i ARG1 -s ARG2 -t ARG3*

where

ARG1 = "path to TAB/Comma seperated file with Adjacency matrix, for eg. data/sample1.tsv"
ARG2 = "Root/Source node of Adjacency matrix"
ARG3 = "Destination/target node of Adjacency matrix"