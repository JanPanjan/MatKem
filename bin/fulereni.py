#!/usr/bin/env python3

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
lines = Lines([[coordinates[u], coordinates[v]] for u, v in edge_list], c='black')

pyramid = {
    1: [2, 4, 5],
    2: [1, 3, 5],
    3: [2, 4, 5],
    4: [1, 3, 5],
    5: [1, 2, 3, 4],
}

pyramid_coordinates = {
    1: (2.0, 0.0, 0.0),
    2: (3.0, 0.0, 0.0),
    3: (3.0, 1.0, 0.0),
    4: (2.0, 1.0, 0.0),
    5: (2.5, 0.5, 1.0),
}

pyramid_coords_list = [pyramid_coordinates[i] for i in range(1, 5 + 1)]
pyramid_edge_list = [(u, v) for v in pyramid for u in pyramid[v] if u < v]

pyramid_points = Points(pyramid_coords_list, r=12, c='red')
pyramid_lines = Lines([[pyramid_coordinates[u], pyramid_coordinates[v]] for u, v in pyramid_edge_list], c='blue')

plt = Plotter()
plt.show(points, lines, pyramid_points, pyramid_lines)

