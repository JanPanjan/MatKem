#!/usr/bin/env python3
import networkx
import sys
import cli
from benzenoids import benparse as bp
from networkx import Graph


def print_help():
    print(f"Usage: {sys.argv[0]} [ *.bec | *.g6 ]")


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
    f = open(file_path, "r")
    l: list[tuple[int, int, str]] = []

    extension = cli.file_ext(file_path)

    if extension == ".bec":
        for bec in f:
            g = bp.from_bec(bec)
            l.append((zagreb_1(g), zagreb_2(g), bec))
    elif extension == ".g6":
        for g6s in f:
            g = bp.from_g6(g6s)
            l.append((zagreb_1(g), zagreb_2(g), g6s))
    else:
        raise ValueError("wrong file extension. Consider renaming to '.bec' or '.g6'")

    f.close()
    l.sort(reverse=True)
    return l


def run(config: cli.Config):
    """ Executes the program logic. """
    ext: str = cli.file_ext(config.file_path)

    if ext == ".bec":
        print("z1 z2 bec")
    else:
        print("z1 z2 g6s")

    zagreb = zagreb_index(config.file_path)

    # gs = graph string 
    for z1, z2, gs in zagreb:
        print(z1, z2, gs.strip())


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    cfg = Config(file_path=sys.argv[1])
    print(cfg)
    run(cfg)