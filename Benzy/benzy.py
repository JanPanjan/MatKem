import sys
import networkx as nx
import matplotlib.pyplot as plt

Cdt = tuple[int, int]  # coordinate


class Benzy():
    """
    Creates a benzenoid system from a BEC that can be plotted.
    """

    def __init__(self, bec: str) -> None:
        self.bec = self.check_bec(bec)
        self.np = sum([int(d) for d in self.bec])  # perimiter nodes
        self.__x = 1
        self.__y = 1
        self.moveset: list[Cdt] = [
            (2 * self.__x, self.__y),    # 1, up-right
            (2 * self.__x, -self.__y),   # 2, down-right
            (0, -2 * self.__y),          # 3, down
            (-2 * self.__x, -self.__y),  # 4, down-left
            (-2 * self.__x, self.__y),   # 5, up-left
            (0, 2 * self.__y),           # 6, up
        ]
        self.graph = self.__graph_from_bec()
        self.coordinates: dict[int, Cdt] = self.__calc_coord()

    def draw_bs(self):
        """
        Plots the benzenoid system.
        """
        nx.draw(
            G=self.graph,
            pos=self.coordinates,
            with_labels=True,
            node_size=700,
            node_color="skyblue",
            font_weight="bold"
        )
        plt.title(f"Benzenoid system of {self.bec}")
        plt.show()

    def check_bec(self, bec: str) -> str:
        for d in bec:
            if not d.isdigit():
                raise ValueError("Illegal boundary edges code. Must be numeric.")
            if int(d) == 6 or int(d) == 0:
                raise ValueError("Illegal boundary edges code. Cannot contain 6 or 0")
        return bec

    def __graph_from_bec(self) -> nx.Graph:
        """
        Creates a networkx graph.
        """
        g = nx.Graph()
        g.add_edges_from([(i, i + 1) for i in range(1, self.np)])
        g.add_edge(self.np, 1)  # connect the graph
        return g

    def __move(self, node: Cdt, move: Cdt) -> Cdt:
        """
        Moves node to new coordinates specified by move (change of x and y)
        """
        return (node[0] + move[0], node[1] + move[1])

    def __next_rotation(self, r: int):
        """
        Gets the next valid rotation, moving to the beginning/end of moveset if necessary.
        """
        r += 1
        match r:
            case 6:
                return 0
            case -1:
                return 5
            case _:
                return r

    def __find_cdt(self, graph: dict[int, Cdt], coordinates: Cdt) -> bool:
        """
        Finds if there already exists an edge with these coordinates.
        """
        for edge_c in graph.values():
            if edge_c == coordinates:
                return True
        else:
            return False

    def __add(
            self,
            node_id: int,
            graph: dict[int, Cdt],
            rotation: int,
            previous: Cdt
    ) -> None:
        move: Cdt = self.moveset[rotation]
        next: Cdt = self.__move(previous, move)
        graph[node_id] = next  # don't bother checking if they already exist...

    def __calc_coord(self) -> dict[int, Cdt]:
        """
        Calculates coordinates for all nodes.
        """
        r = 0  # starting rotation
        i = 1  # starting node
        sc: Cdt = (0, 0)  # starting coordinates
        pos: dict[int, Cdt] = {i: sc}  # starting position

        for digit in self.bec:
            digit = int(digit)
            for _ in range(digit):
                i += 1
                self.__add(i, pos, r, sc)
                r = self.__next_rotation(r)
                sc = pos[i]
            # save values for next digit
            r -= 2

        return pos


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: benzy.py [int | list[int]]""")
        print("Examples:", end=" ")
        for e in ["55", "2525", "333333", "444" "5312351231"]:
            print(e, end=" ")
        print()

    for b in sys.argv[1:]:
        g = Benzy(b)
        g.draw_bs()
