#!/usr/bin/env python3
import networkx
import pathlib
import sys
import benparse as bp
from networkx import Graph
from typing import NamedTuple

class Config(NamedTuple):
    file_path: str
    mode: str

def print_help():
    """Prints help about the program usage."""
    print(f"Usage: {sys.argv[0]} <file> <index>")
    print("index : [ zagreb | wiener ]")
    print("file  : [ *.bec | *.g6 ]")

def file_ext(file_path: str) -> str:
    """Returns file extension."""
    return pathlib.Path(file_path).suffix

def zagreb_1(g: Graph):
    """Calculates Zagreb 1 index for the given graph."""
    s = 0
    for v in g.nodes():
        s += g.degree(v) ** 2
    return s

def zagreb_2(g: Graph):
    """Calculates Zagreb 2 index for the given graph."""
    s = 0
    for u, v in g.edges():
        s += g.degree(v) * g.degree(u)
    return s

def zagreb_index(file_path: str) -> list[tuple[int, int, str]]:
    """Calculates Zagreb indexes for each G6 graph stored in the file.

    :param file_path: path to file
    """
    ext: str = file_ext(file_path)
    f = open(file_path, "r")
    l: list[tuple[int, int, str]] = []

    match ext:
        case ".bec":
            for bec in f:
                g = bp.from_bec(bec)
                l.append((zagreb_1(g), zagreb_2(g), bec))
        case ".g6":
            for g6s in f:
                g = bp.from_g6(g6s)
                l.append((zagreb_1(g), zagreb_2(g), g6s))
        case _:
            raise ValueError("wrong file extension. Consider renaming to '.bec' or '.g6'")

    f.close()
    l.sort(reverse=True)
    return l

def wiener_index(file_path: str) -> list[tuple[float, str]]:
    """Calculates Wiener index for each G6 graph stored in the file.

    :param file_path: path to file
    """
    ext: str = file_ext(file_path)
    f = open(file_path, "r")
    l: list[tuple[float, str]] = []

    match ext:
        case ".bec":
            for bec in f:
                g = bp.from_bec(bec)
                l.append((networkx.wiener_index(g), bec))
        case ".g6":
            for g6s in f:
                g = bp.from_g6(g6s)
                l.append((networkx.wiener_index(g), g6s))
        case _:
            raise ValueError("wrong file extension. Consider renaming to '.bec' or '.g6'")

    f.close()
    l.sort(reverse=True)
    return l

"""
cubic graphs: each edge is of degree 3, can't have odd number of edges
trees:        number of edges is 1 less than number of nodes
"""
if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[2] not in ["zagreb", "wiener"]:
        print_help()
        sys.exit(1)

    cfg = Config(file_path=sys.argv[1], mode=sys.argv[2])
    print(cfg)
    ext: str = file_ext(cfg.file_path)

    # gs = graph string (can be g6 or bec)
    match cfg.mode:
        case "zagreb":
            if ext == ".bec":
                print("z1 z2 bec")
            else:
                print("z1 z2 g6s")

            zagreb = zagreb_index(cfg.file_path)

            for z1, z2, gs in zagreb:
                print(z1, z2, gs.strip())

        case "wiener":
            if ext == ".bec":
                print("wi bec")
            else:
                print("wi g6s")

            wiener = wiener_index(cfg.file_path)

            for wi, gs in wiener:
                print(wi, gs.strip())
