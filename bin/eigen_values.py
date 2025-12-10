#!/bin/python3

import numpy as np
import networkx as nx
from pprint import pprint

# g = nx.Graph([(1,2), (2,3), (3,4)])

AAA = nx.Graph([
    (1,2), (1,5), (1,8),
    (2,3), (2,6),
    (3,4),
    (4,5),
    (6,7),
    (7,8)
])

benzene = nx.Graph([
    (1,2),
    (2,3),
    (3,4),
    (4,5),
    (5,6),
    (6,1),
])
c7 = nx.Graph([
    (1,2),
    (2,3),
    (3,4),
    (4,5),
    (5,6),
    (6,7),
    (7,1),
])
cubane = nx.Graph([
    (1,2),
    (1,6),
    (1,4),
    (2,7),
    (2,3),
    (3,8),
    (3,4),
    (4,5),
    (5,6),
    (5,8),
    (6,7),
    (7,8),
])

def eig(g: nx.Graph) -> None:
    A = nx.to_numpy_array(g)
    eigval, eigvec = np.linalg.eigh(A)
    eigval, eigvec = (np.round(eigval, 2), np.round(eigvec, 2))


    print("eig values:\n\n", eigval, end="\n\n")
    print("eig vectors:\n")
    for i, _ in enumerate(eigvec):
        print(i, eigvec[:, i])
    print("\n")

if __name__ == "__main__":
    print("-------------------- benzene --------------------")
    eig(benzene)
    print("-------------------- cubane --------------------")
    eig(cubane)
    print("-------------------- c7 --------------------")
    eig(c7)