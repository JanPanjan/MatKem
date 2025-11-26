#!/usr/bin/env python3
import networkx
import sys


def print_help():
    print(f"Usage: {sys.argv[0]} <file> <index>")
    print("Index can be 'zagreb' or 'wiener'")


def zagreb_1(g):
    s = 0
    for v in g.nodes():
        s += g.degree(v)**2
    return s

def zagreb_2(g):
    s = 0
    for u, v in g.edges():
        s += g.degree(v) * g.degree(u)
    return s


def get_zagreb_index(file_path: str) -> list[tuple[int, int, str]]:
    f = open(f_name, 'r')
    l = []
    for line in f:
        g6s = line.strip()
        g = networkx.from_graph6_bytes(g6s.encode('ascii'))
        l.append((zagreb_1(g), zagreb_2(g), g6s))
    f.close()
    l.sort(reverse=True)
    return l


def get_wiener_index(file_path: str) -> list[tuple[int, str]]:
    f = open(f_name, 'r')
    l = []
    for line in f:
        g6s = line.strip()
        g = networkx.from_graph6_bytes(g6s.encode('ascii'))
        l.append((networkx.wiener_index(g), g6s))
    f.close()
    return l


"""
cubic graphs: each edge is of degree 3, can't have odd number of edges
trees: number of edges is 1 less than number of nodes
"""
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_help()
        sys.exit(1)
    if sys.argv[2] not in ["zagreb", "wiener"]:
        print_help()
        sys.exit(1)

    f_name = sys.argv[1]

    match sys.argv[2]:
        case "zagreb":
            zagreb = get_zagreb_index(f_name)
            for z1, z2, g6s in zagreb:
                print(z1, z2, g6s)
        case "wiener":
            wiener = get_wiener_index(f_name)
            for z, g6s in wiener:
                print(z, g6s)

