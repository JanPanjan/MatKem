#!/usr/bin/env python3
import sys
import cli
from cli import ArgumentError
from indexes import wiener, zagreb

HELP = f"Usage: {sys.argv[0]} [ zagreb | wiener ] [ *.bec | *.g6 ]"

"""
cubic graphs: each edge is of degree 3, can't have odd number of edges
trees:        number of edges is 1 less than number of nodes
"""
if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise cli.ArgumentError("Not enough arguments", HELP)

    mode = sys.argv[1]
    file_path = sys.argv[2]
    ext: str = cli.file_ext(file_path)

    if mode not in ["zagreb", "wiener"]:
        raise ArgumentError(f"Wrong mode: '{mode}'.", HELP)

    if ext != ".bec" and ext != ".g6":
        raise ArgumentError(f"Wrong file format: '{ext}'.", HELP)

    match mode:
        case "zagreb": zagreb.run(cli.Config(file_path))
        case "wiener": wiener.run(cli.Config(file_path))
        case _: raise Exception("wrong mode")
