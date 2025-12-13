#!/bin/python3

import numpy as np
import networkx as nx

# g = nx.Graph([(1,2), (2,3), (3,4)])

AAA = nx.Graph([
    (1, 2), (1, 5), (1, 8),
    (2, 3), (2, 6),
    (3, 4),
    (4, 5),
    (6, 7),
    (7, 8)
])

benzene = nx.Graph([
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 5),
    (5, 6),
    (6, 1),
])
c7 = nx.Graph([
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 1),
])
cubane = nx.Graph([
    (1, 2),
    (1, 6),
    (1, 4),
    (2, 7),
    (2, 3),
    (3, 8),
    (3, 4),
    (4, 5),
    (5, 6),
    (5, 8),
    (6, 7),
    (7, 8),
])


def eigs(g: nx.Graph) -> tuple[np.ndarray, np.ndarray]:
    """ Returns eigen values and eigen vectors of a graph. """
    A = nx.to_numpy_array(g)
    eigval, eigvec = np.linalg.eigh(A)
    eigval, eigvec = (np.round(eigval, 2), np.round(eigvec, 2))
    return (eigval, eigvec)


def neutral_configuration(g: nx.Graph) -> list[int]:
    """ Returns neutral configuration based on eigen values (reverse order). """
    eigval, _ = eigs(g)
    nc = {}
    for v in eigval:
        if v not in nc:
            nc[v] = 1
        else:
            nc[v] += 1
    return list(nc.values())


def total_pi_charge(g: nx.Graph) -> list[float]:
    """ Returns total pi charge for each eigen vector. """
    total = 0
    nc = neutral_configuration(g)
    for i in range(len(nc)-1, -1, -1):
        for r in range(nc[i]):
            print(r, end=" ")
        print()


def eig(g: nx.Graph) -> None:
    eigval, eigvec = eigs(g)

    print("eig values:\n\n", eigval, end="\n\n")
    print("eig vectors:\n")
    for i, _ in enumerate(eigvec):
        print(i, eigvec[:, i])
    print("\n")


if __name__ == "__main__":
    """ 
    print("-------------------- benzene --------------------")
    eig(benzene)
    print("-------------------- cubane --------------------")
    eig(cubane)
    print("-------------------- c7 --------------------")
    eig(c7)
    """
    # nc_b = neutral_configuration(benzene)
    total_pi_charge(benzene)
    # print(nc_b)