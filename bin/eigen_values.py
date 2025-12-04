#!/bin/python3

import numpy as np
import networkx as nx
from pprint import pprint

# g = nx.Graph([(1,2), (2,3), (3,4)])

g = nx.Graph([
    (1,2), (1,5), (1,8),
    (2,3), (2,6),
    (3,4),
    (4,5),
    (6,7),
    (7,8)
])

A = nx.to_numpy_array(g)
eigval, eigvec = np.linalg.eigh(A)

print("eig values:\n", eigval, end="\n\n")
print("eig vectors:\n")
for i, _ in enumerate(eigvec):
    print(i+1, eigvec[:, i])