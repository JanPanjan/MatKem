import networkx as nx
import matplotlib.pyplot as plt
from typing import NamedTuple


class Node(NamedTuple):
    x: int
    y: int


def graph_from_bec(bec: str) -> nx.Graph:
    g = nx.Graph()
    n = sum([int(d) for d in bec])  # number of perimiter nodes
    g.add_edges_from([(i, i + 1) for i in range(1, n)])
    g.add_edge(n, 1)
    return g


def draf_bs(g, pos):
    nx.draw(
        g,
        pos=pos,
        with_labels=True,
        node_size=800,    # Adjust node size
        node_color='skyblue',
        font_weight='bold'
    )
    plt.title("Graph with Custom Node Positions")
    plt.show()


def get_coordinates(bec: str) -> dict:
    x = 1
    y = 1
    HM = {
        "UR": Node(x, y),    # up-right
        "UL": Node(-x, y),   # up-left
        "DR": Node(x, -y),   # down-right
        "DL": Node(-x, -y),  # down-left
        "UU": Node(0, y),    # up
        "DD": Node(0, -y)    # down
    }

    steps = {  # keys = steps
        1: {  # keys = rotacije
            0: [HM["UR"]],  # vsak element seznama pove kako dobiš novo koordinato
            1: [HM["UU"]],
            2: [HM["UL"]],
            3: [HM["DL"]],
            4: [HM["UL"]],
            5: [HM["DR"]],
            6: [HM["DD"]]
        },
        2: {
            0: [HM["UR"], HM["DR"]],
            1: [HM["UU"], HM["UR"]],
            2: [HM["UL"], HM["UU"]],
            3: [HM["DL"], HM["UL"]],
            4: [HM["UL"], HM["UU"]],
            5: [HM["DR"], HM["UL"]],
            6: [HM["DR"], HM["DD"]],
        },
        3: {
            0: [HM["UR"], HM["DR"], HM["DD"]],
            1: [HM["UU"], HM["UR"], HM["DR"]],
            2: [HM["UL"], HM["UU"], HM["UR"]],
            3: [HM["DL"], HM["UL"], HM["UU"]],
            # 4: [HM["UL"], HM["DL"], HM["UL"]],
            4: [HM["UL"], HM["UU"], HM["UR"]],
            5: [HM["DR"], HM["UL"], HM["UU"]],
            6: [HM["DR"], HM["DD"]],
        },
        4: {
            0: [HM["UR"], HM["DR"], HM["DD"], HM["DL"]],
            1: [HM["UU"], HM["UR"], HM["DR"], HM["DD"]],
            2: [HM["UL"], HM["UU"], HM["UR"], HM["DR"]],
            3: [HM["DL"], HM["UL"], HM["UU"], HM["UR"]],
            # 4: [HM["UL"], HM["DL"], HM["UL"], HM["UU"]],
            4: [HM["UL"], HM["UU"], HM["UR"], HM["DR"]],
            5: [HM["DR"], HM["UL"], HM["UU"], HM["UL"]],
            6: [HM["DR"], HM["DD"]],
        },
        5: {
            0: [HM["UR"], HM["DR"], HM["DD"], HM["DL"], HM["UL"]],
            1: [HM["UU"], HM["UR"], HM["DR"], HM["DD"], HM["DL"]],
            2: [HM["UL"], HM["UU"], HM["UR"], HM["DR"], HM["DD"]],
            3: [HM["DL"], HM["UL"], HM["UU"], HM["UR"], HM["DR"]],
            # 4: [HM["UL"], HM["DL"], HM["UL"], HM["UU"], HM["UR"]],
            4: [HM["UL"], HM["UU"], HM["UR"], HM["DR"], HM["DD"]],
            5: [HM["DR"], HM["UL"], HM["UU"], HM["UL"], HM["DL"]],
            6: [HM["DR"], HM["DD"]],
        }
    }

    def move_node(node: Node, move: Node) -> Node:
        return (node[0] + move.x,
                node[1] + move.y)

    rotation = (-1, 0, 1, 2, 3, 1)
    r = 0
    i = 1
    pos = {i: Node(0, 0)}  # starting position
    for d in bec:
        d = int(d)
        print("node:", i, ", d:", d, ", rotation:", r, end="")
        moveset: list[Node] = steps[d][r]
        print(", moveset:", moveset)
        for move in moveset:
            pos[i + 1] = move_node(pos[i], move)
            i += 1
        r += rotation[d - 1]  # since it's 1-based
        if r >= 6:
            r -= 6
    return pos


if __name__ == "__main__":
    bec = "333333"
    print(bec)
    g = graph_from_bec(bec)
    pos = get_coordinates(bec)
    print(pos)
    draf_bs(g, pos)
