#!/bin/python3

import numpy as np
import networkx as nx

cube = nx.Graph([
    (1, 2), (2, 3), (3, 4), (4, 1)
])

benzenoid_linear_2 = nx.Graph([
    (1, 2), (1, 6), (1, 10),
    (2, 3), (2, 7),
    (3, 4),
    (4, 5),
    (5, 6),
    (7, 8),
    (8, 9),
    (9, 10),
])

bicyclo_octane = nx.Graph([
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
    v = [0] * len(eigval) # vector for neutral configuration
    frq = {}

    for val in eigval:
        if val not in frq:
            frq[val] = 1
        else:
            frq[val] += 1

    ncc = list(frq.values())
    cur_id = 0
    num_orb = len(eigval)
    # print("num orb:", num_orb, "ncc:", ncc)

    for n in ncc:
        r = range(cur_id, cur_id + n)
        fill = 2 * n
        # print("n:", n)
        # print("range:", r)
        # print("cur_id:", cur_id)
        while fill > 0 and num_orb > 0:
            b = False
            for _ in range(n):
                for i in r:
                    v[i] += 1
                    fill -= 1
                    num_orb -= 1
                    if num_orb == 0:
                        b = True
                        break
                if b:
                    break
                # print(" v:", v, end=",")
                # print(" fill:", fill)
        cur_id += n

    return v


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
    print("-------------------- cube --------------------")
    eig(cube)
    print("neutral configuration:", neutral_configuration(cube), end="\n\n")

    print("-------------------- linear benzenoid 2 --------------------")
    eig(benzenoid_linear_2)
    print("neutral configuration:", neutral_configuration(benzenoid_linear_2), end="\n\n")

    print("-------------------- bicyclo octane --------------------")
    eig(bicyclo_octane)
    print("neutral configuration:", neutral_configuration(bicyclo_octane), end="\n\n")

    print("-------------------- benzene --------------------")
    eig(benzene)
    print("neutral configuration:", neutral_configuration(benzene), end="\n\n")

    print("-------------------- cubane --------------------")
    eig(cubane)
    print("neutral configuration:", neutral_configuration(cubane), end="\n\n")

    print("-------------------- c7 --------------------")
    eig(c7)
    print("neutral configuration:", neutral_configuration(c7), end="\n\n")