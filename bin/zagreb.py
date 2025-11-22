#!/usr/bin/env python3
import networkx
import sys


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


f_name = sys.argv[1]
f = open(f_name, 'r')

ms = []

for line in f:
    g6s = line.strip()
    g = networkx.from_graph6_bytes(g6s.encode('ascii'))
    ms.append((zagreb_1(g), zagreb_2(g), g6s))
f.close()

ms.sort(reverse=True)


# if len(ms) < 4:
#     for m1, m2, g6 in ms:
#         print(m1, m2, g6)
# else:

print(sys.argv[1], "\n")

for z1, z2, g6s in ms:
    print(z1, z2, g6s)

print()
