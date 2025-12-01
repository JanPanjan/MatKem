#!/usr/bin/env python3
import networkx
import sys
import cli
from benzenoids import benparse as bp
from networkx import Graph


def print_help():
    print(f"Usage: {sys.argv[0]} [ *.bec | *.g6 ]")


def wiener_index(file_path: str) -> list[tuple[float, str]]:
    """Calculates Wiener index for each G6 graph stored in the file.

    :param file_path: path to file
    """
    f = open(file_path, "r")
    l: list[tuple[float, str]] = []

    extension = cli.file_ext(file_path)

    if extension == ".bec":
        for bec in f:
            g = bp.from_bec(bec)
            l.append((networkx.wiener_index(g), bec))
    elif extension == ".g6":
        for g6s in f:
            g = bp.from_g6(g6s)
            l.append((networkx.wiener_index(g), g6s))
    else:
        raise ValueError("wrong file extension. Consider renaming to '.bec' or '.g6'")

    f.close()
    l.sort(reverse=True)
    return l


def run(config: cli.Config):
    """ Executes the program logic. """
    ext: str = cli.file_ext(config.file_path)

    if ext == ".bec":
        print("wi bec")
    else:
        print("wi g6s")

    wiener = wiener_index(config.file_path)

    # gs = graph string 
    for wi, gs in wiener:
        print(wi, gs.strip())


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    cfg = cli.Config(file_path=sys.argv[1])
    print(cfg)
    run(cfg)