#!/usr/bin/env python3

import sys
import networkx
import numpy


def read_plc(f_name):
    f_in = open(f_name, "rb")
    header = ">>planar_code<<"
    if f_in.read(len(header)).decode() != header:
        raise ValueError("missing header")
    while True:
        n_byte = f_in.read(1)
        if len(n_byte) == 0:
            break  # End of file
        b_mode = 1
        n = int.from_bytes(n_byte, byteorder="little", signed=False)
        if n == 0:
            b_mode = 2
            n = int.from_bytes(f_in.read(2), byteorder="little", signed=False)
        g = {i: [] for i in range(1, n + 1)}
        for i in range(1, n + 1):
            while True:
                neigh = int.from_bytes(
                    f_in.read(b_mode), byteorder="little", signed=False
                )
                if neigh == 0:
                    break
                g[i].append(neigh)
        yield g
    f_in.close()


def all_kekule_structures(g):
    if len(g) % 2 != 0:
        return []  # No Kekule structures if odd number of vertices.
    matchings = []

    def branch(g_sub, current_matching):
        if len(g_sub.nodes) == 0:
            matchings.append(current_matching.copy())
            return
        if len(g_sub.edges) == 0:
            return
        # Check for vertex of degree 1
        deg1_nodes = [n for n in g_sub.nodes if g_sub.degree[n] == 1]
        if deg1_nodes:
            u = deg1_nodes[0]
            v = next(g_sub.neighbors(u))
            new_matching = current_matching + [(u, v)]  # Include this edge
            g_next = g_sub.copy()
            g_next.remove_nodes_from([u, v])
            branch(g_next, new_matching)
            return
        # No forced edges, pick an arbitrary edge
        u, v = next(iter(g_sub.edges))
        # Branch 1: include edge (u,v)
        g_include = g_sub.copy()
        g_include.remove_nodes_from([u, v])
        branch(g_include, current_matching + [(u, v)])
        # Branch 2: exclude edge (u,v)
        g_exclude = g_sub.copy()
        g_exclude.remove_edge(u, v)
        branch(g_exclude, current_matching)

    branch(g.copy(), [])
    return matchings


def number_of_kek_str(g):
    adj = networkx.to_numpy_array(g)
    kek = abs(numpy.linalg.det(adj)) ** 0.5
    return round(kek)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            """
    Calculate number of fixed double bonds present in given kekule structures

    Usage: ./fixed_double_bonds.py <plc-code>
        """
        )
        sys.exit()
    f_name = sys.argv[1]
    for g_adj in read_plc(f_name):
        g = networkx.nx.nx.Graph(g_adj)
        # kek1 = number_of_kek_str(g)
        kek_list = all_kekule_structures(g)
        k = len(kek_list)
        g6 = networkx.to_nx.Graph6_bytes(g).decode().strip()
        # print('Number of Kekule structures:', kek1, kek2)
        freq = {}
        for kek in kek_list:
            skek = [tuple(sorted([u, v])) for u, v in kek]
            for edge in skek:
                freq[edge] = freq.get(edge, 0) + 1
        # print(k)
        # print(freq)
        fixed_double = []
        for edge in freq:
            if freq[edge] == k:
                fixed_double.append(edge)
        if len(fixed_double) > 0:
            print(g6)
            print(len(fixed_double), fixed_double)
