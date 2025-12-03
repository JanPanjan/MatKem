#!/bin/python3

import numpy as np
import networkx as nx

g = nx.Graph([(1,2), (2,3), (3,4)])
A = nx.to_numpy_array(g)

eigval, eigvec = np.linalg.eigh(A)

print("\n" ,eigval)
print("\n", eigvec)