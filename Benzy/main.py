#!/usr/bin/env python3

import sys
import networkx
import matplotlib.pyplot as plt


def print_help():
    PNAME = "main.py"
    print("Usage:")
    print(f"  {PNAME} c <*.plc>")
    print(f"  {PNAME} v <*.plc> <*.bec>")
    print("Mode:")
    print("  c - cli (Kekulé Count)")
    print("  v - visual (Benzenoid Layout)")


def read_plc(f_name):
    """Reads the planar code (.plc) file format."""
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


def read_bec(f_name: str) -> list[str]:
    """Reads the BEC file, returning a list of raw string segments (one per line)."""
    with open(f_name, 'r') as f:
        return [l.strip() for l in f.readlines()]


def all_kekule_structures(g):
    if len(g) % 2 != 0:
        return []
    matchings = []

    def branch(g_sub, current_matching):
        if len(g_sub.nodes) == 0:
            matchings.append(current_matching.copy())
            return
        if len(g_sub.edges) == 0:
            return
        deg1_nodes = [n for n in g_sub.nodes if g_sub.degree[n] == 1]
        if deg1_nodes:
            u = deg1_nodes[0]
            try:
                v = next(g_sub.neighbors(u))
            except StopIteration:
                return
            new_matching = current_matching + [(u, v)]
            g_next = g_sub.copy()
            g_next.remove_nodes_from([u, v])
            branch(g_next, new_matching)
            return
        u, v = next(iter(g_sub.edges))
        g_include = g_sub.copy()
        g_include.remove_nodes_from([u, v])
        branch(g_include, current_matching + [(u, v)])
        g_exclude = g_sub.copy()
        g_exclude.remove_edge(u, v)
        branch(g_exclude, current_matching)

    branch(g.copy(), [])
    return matchings


def calculate_benzenoid_positions():
    pass


def draw_graph(graph: networkx.Graph, bec_list: list[int] = None):
    pos = calculate_benzenoid_positions(graph, bec_list)
    plt.figure(figsize=(8, 8))
    networkx.draw(
        graph,
        pos,
        with_labels=True,
        node_color='skyblue',
        node_size=800,
        edge_color='black',
        linewidths=2,
        font_weight='bold'
    )
    plt.title(f"Benzenoid Visualization, BEC: {''.join(bec_list)}")
    plt.savefig("benzene_matplotlib.png")
    plt.show()

    if input("Enter: next, q: exit > ") == "q":
        sys.exit()


def visual_mode(fbec: str, fplc: str):
    bec_iter = iter(read_bec(fbec))
    for g_adj in read_plc(fplc):
        g = networkx.Graph(g_adj)
        print(g.nodes())
        print(g.edges())
        # bec_list: list[int] = [int(d) for d in bec_iter.__next__()]
        # draw_graph(g, bec_list)


def cli_mode(fplc: str):
    for g_adj in read_plc(fplc):
        g = networkx.Graph(g_adj)
        kek_list = all_kekule_structures(g)
        k = len(kek_list)
        g6 = networkx.to_graph6_bytes(g).decode().strip()
        freq = {}
        for kek in kek_list:
            skek = [tuple(sorted([u, v])) for u, v in kek]
            for edge in skek:
                freq[edge] = freq.get(edge, 0) + 1

        fixed_double = []
        for edge in freq:
            if freq[edge] == k:
                fixed_double.append(edge)

        if len(fixed_double) > 0:
            print(g6)
            print(len(fixed_double), fixed_double)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print_help()
        sys.exit()

    mode = sys.argv[1]

    if mode == 'c':
        if len(sys.argv) != 3:
            print_help()
            sys.exit()
        fplc = sys.argv[2]
        cli_mode(fplc)

    elif mode == 'v':
        if len(sys.argv) != 4:
            print_help()
            sys.exit()
        fplc = sys.argv[2]
        fbec = sys.argv[3]
        visual_mode(fbec, fplc)

    else:
        print_help()
        sys.exit()
