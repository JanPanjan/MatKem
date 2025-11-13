#!/usr/bin/env python3
import sys
import networkx
from pprint import pprint


def read_plc(f_name):
    f_in = open(f_name, 'rb')
    header = '>>planar_code<<'
    if f_in.read(len(header)).decode() != header:
        raise ValueError('missing header')
    while True:
        n_byte = f_in.read(1)
        if len(n_byte) == 0:
            break  # End of file
        b_mode = 1
        n = int.from_bytes(n_byte, byteorder='little', signed=False)
        if n == 0:
            b_mode = 2
            n = int.from_bytes(f_in.read(2), byteorder='little', signed=False)
        g = {i: [] for i in range(1, n + 1)}
        for i in range(1, n + 1):
            while True:
                neigh = int.from_bytes(f_in.read(b_mode), byteorder='little', signed=False)
                if neigh == 0:
                    break
                g[i].append(neigh)
        yield g
    f_in.close()


def inverse(dart):
    u, v = dart
    return (v, u)


def next_in_rotation(rotation, dart):
    '''Return the next dart around vertex dart[0].'''
    u, v = dart
    order = rotation[u]
    i = order.index(v)
    return (u, order[(i + 1) % len(order)])


def compute_faces(rotation):
    '''Return a list of faces, each represented as a list of darts (u,v).'''
    darts = {(u, v) for u in rotation for v in rotation[u]}
    visited = set()
    faces = []

    for dart in darts:
        if dart in visited:
            continue
        face = []
        d = dart
        while d not in visited:
            visited.add(d)
            face.append(d)
            d = next_in_rotation(rotation, inverse(d))
        faces.append(face)
    return faces


def dual_rotation(rotation):
    '''Compute the dual rotation system and outer face index.'''
    faces = compute_faces(rotation)
    # Number faces 0 ... n-1
    n_faces = len(faces)
    outer_face = max(range(n_faces), key=lambda i: len(faces[i]))

    # Map each dart to the face it belongs to
    dart_to_face = {}
    for i, face in enumerate(faces):
        for dart in face:
            dart_to_face[dart] = i

    # Build dual rotation: each face -> cyclic list of neighboring faces
    dual = {i: [] for i in range(n_faces)}
    for i, face in enumerate(faces):
        for dart in face:
            inv = inverse(dart)
            if inv in dart_to_face:
                neighbor = dart_to_face[inv]
                dual[i].append(neighbor)

    return dual, outer_face


if __name__ == '__main__':
    for g_adj in read_plc(sys.argv[1]):
        g_dual = dual_rotation(g_adj)
        # print(g_adj)
        print(g_dual)
