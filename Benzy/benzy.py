import networkx as nx
import matplotlib.pyplot as plt


def graph_from_bec(bec: str) -> nx.Graph:
    """ Creates graph from BEC string """
    g = nx.Graph()
    n = sum([int(d) for d in bec])  # number of perimiter nodes
    g.add_edges_from([(i, i + 1) for i in range(1, n)])
    g.add_edge(n, 1)
    return g


def draw_bs(g: nx.Graph, pos: dict[int, tuple[int, int]]):
    """ Draws the benzenoid system g based on positions pos """
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


def move_node(node: tuple[int, int], move: tuple[int, int]) -> tuple[int, int]:
    """ Moves node to new coordinates """
    return (node[0] + move[0], node[1] + move[1])


def get_coordinates(bec: str) -> dict:
    """ Calculates coordinates for benzenoid system """
    x = 1
    y = 1
    MOVESET = [
        (x,   y),  # 1, up-right
        (x,  -y),  # 2, down-right
        (0,  -y),  # 3, down
        (-x, -y),  # 4, down-left
        (-x,  y),  # 5, up-left
        (0,   y),  # 6, up
    ]

    ROTATION = (-1, 0, 1, 2, 3, -1)
    r = 0              # starting rotation
    i = 1              # starting node
    pos = {i: (0, 0)}  # starting position

    for d in bec:
        d = int(d)                         
        print("node:", i, ", d:", d, ", rotation:", r)
        for _ in range(d):  # just go through all additions
            print(i+1, r, end=" ")
            print (MOVESET[r])
            pos[i + 1] = move_node(pos[i], MOVESET[r])
            # if r becomes negative, take the corresponding move from the back
            # e.g., r=-2 implies MOVESET[-2]=MOVESET[5]=(-x,y)
            i += 1
            r += 1
            if r == 6: r = 0
            elif r == -1: r = 5
        r -= 2
    return pos


if __name__ == "__main__":
    bec = "4343"
    print(bec)
    g = graph_from_bec(bec)
    pos = get_coordinates(bec)
    print(pos)
    draw_bs(g, pos)
