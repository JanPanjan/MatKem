"""Module for parsing different benzenoid graph formats into `nx.Graph`"""
import networkx as nx
import sys

def from_g6(raw_g6: str) -> nx.Graph:
    """Creates a `nx.Graph.` from a g6 string."""
    g6s: str = raw_g6.strip()
    g = nx.from_graph6_bytes(g6s.encode("ascii"))

    return g

def from_bec(raw_bec: str) -> nx.Graph:
    """Creates a `nx.Graph.` from a BEC string."""
    bec: str = _check_bec(raw_bec)
    perimiter_vertices: int = sum(int(d) for d in bec)
    g: nx.Graph = nx.Graph()

    g.add_edges_from([(i, i + 1) for i in range(1, perimiter_vertices)])
    g.add_edge(perimiter_vertices, 1)  # connect the nx.Graph

    return g

def _check_bec(raw_bec: str) -> str:
    """Makes sure the provided BEC is valid.

    Valid BEC is composed only of numbers between 1-5.
    """
    bec: str = raw_bec.strip()

    try:
        for d in bec:
            if int(d) == 6 or int(d) == 0:
                raise ValueError("Illegal boundary edges code. Cannot contain 6 or 0")
    except Exception as e:
        raise Exception(f"Error occured: {e}")

    return bec
