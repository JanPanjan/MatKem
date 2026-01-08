#!/usr/bin/env python3
import sys
import numpy as np
from vedo import *

cube = {
    1: [2, 4, 5],
    2: [1, 3, 6],
    3: [2, 4, 7],
    4: [1, 3, 8],
    5: [1, 6, 8],
    6: [2, 5, 7],
    7: [3, 6, 8],
    8: [4, 5, 7],
}

coordinates = {
    1: (0, 0, 0),
    2: (1, 0, 0),
    3: (1, 0, 1),
    4: (0, 0, 1),
    5: (0, 1, 0),
    6: (1, 1, 0),
    7: (1, 1, 1),
    8: (0, 1, 1),
}

coordinates_list = [coordinates[i] for i in range(1, 8 + 1)]
edge_list = [(u, v) for v in cube for u in cube[v] if u < v]

points = Points(coordinates_list, r=10, c='green')
lines = Lines([[coordinates[u], coordinates[v]] for u, v in edge_list])

# plt = Plotter()
# plt.show(points, lines)
# pip3 install vedo
# ./fullgen 100 code 6 symm D2d > fulereni_n100_D2d.txt

def load_fullerenes(file_name):
    f = open(file_name, 'r')
    lst = []
    g = {}
    while True:
        line = f.readline().strip()
        if line == '':
            break
        if line.startswith('>>writegraph3d'):
            continue
        tok = [int(x) for x in line.split()]
        if len(tok) == 1:
            lst.append(g)
            g = {}
        else:
            v = tok[0]
            neigh = tok[4:]
            g[v] = neigh
    f.close()
    return lst

def adjacency_matrix(g):
    n = len(g)
    A = np.zeros((n, n))
    for u in g:
        for v in g[u]:
            A[u - 1][v - 1] = 1.0
    return A

def get_coordinates(g, kx, ky, kz):
    A = adjacency_matrix(g)
    n = len(g)
    eigval, eigvec = np.linalg.eigh(A)
    sx = (eigval[n - 1] - eigval[n - kx])**-0.5
    sy = (eigval[n - 1] - eigval[n - ky])**-0.5
    sz = (eigval[n - 1] - eigval[n - kz])**-0.5
    coords = {i: (eigvec[i - 1, n - kx],
                  eigvec[i - 1, n - ky],
                  eigvec[i - 1, n - kz]) for i in range(1, n + 1)}
    return coords

f_list = load_fullerenes(sys.argv[1])
total = len(f_list)

for index, ful in enumerate(f_list):
    n = len(ful)
    coords = get_coordinates(ful, 2, 3, 4)
    coordinates_list = [coords[i] for i in range(1, n + 1)]
    edge_list = [(u, v) for v in ful for u in ful[v] if u < v]

    points = Points(coordinates_list, r=6, c='black')
    lines = Lines([[coords[u], coords[v]] for u, v in edge_list])

    plt = Plotter()
    plt.show(points, lines, f'Fulerene {index + 1} of {total}')
    break
