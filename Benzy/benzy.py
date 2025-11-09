import sys
import networkx as nx
import matplotlib.pyplot as plt

Crd = tuple[int, int]  # coordinate
Vtx = int  # vertex
CrdLst = dict[Vtx, Crd]  # list of coordinates for every vertex


class Benzy():
    """
    Creates a benzenoid system from a BEC that can be plotted.
    """

    def __init__(self, bec: str) -> None:
        self.bec: str = self.check_bec(bec)
        self.np = sum([int(d) for d in self.bec])  # perimiter nodes
        self.__x = 1
        self.__y = 1
        self.moveset: list[Crd] = [
            (2 * self.__x, self.__y),    # 1, up-right
            (2 * self.__x, -self.__y),   # 2, down-right
            (0, -2 * self.__y),          # 3, down
            (-2 * self.__x, -self.__y),  # 4, down-left
            (-2 * self.__x, self.__y),   # 5, up-left
            (0, 2 * self.__y),           # 6, up
        ]
        self.graph: nx.Graph = self.__graph_from_bec()
        self.coordinates: CrdLst = self.__calc_coord()

    def draw_bs(self) -> None:
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

    def __find_cdt(self, graph: CrdLst, coordinates: Crd) -> bool:
        """
        Finds a vertex with these coordinates (or not).
        """
        for edge_c in graph.values():
            if edge_c == coordinates:
                return True
        else:
            return False

    def __find_vtx(self, v: Vtx) -> bool:
        """
        Finds vertex in the graph (or not)
        """
        return v in self.graph

    def __add_cdt(
            self,
            node_id: int,
            cds: CrdLst,
            rotation: int
    ) -> None:
        cds[node_id] = self.__move(cds[node_id - 1], self.moveset[rotation])
        return

    def __move(self, node: Crd, move: Crd) -> Crd:
        """
        Moves node to new coordinates specified by move (change of x and y)
        """
        return (node[0] + move[0], node[1] + move[1])

    def __next_rotation(self, r: int):
        """
        Gets the next valid rotation, moving to the beginning/end of moveset if necessary.

        The first calculated coordinate will always be done by an up-right move.
        First calculated coordinate after a new digit is read will always be done
        with a move 2 steps back in the moveset.
        """
        r += 1
        match r:
            case 6:
                return 0
            case -1:
                return 5
            case _:
                return r

    def __search_nodes(self, clst: CrdLst) -> CrdLst:
        raise NotImplementedError

    def __fill_me_up(self, clst: CrdLst) -> CrdLst:
        """
        Fills up the coordinate list with missing edges and vertices, since
        the original list contains only vertices and edges that form the
        boundary.
        It moves from top left-most coordinate, to bottom right-most. E.g.:

                             ×
            from this --> ×     ×
                          |     |

                            ...   ...

                                |     |
                                ×     × <-- to this
                                   ×
        """
        raise NotImplementedError

    def __calc_coord(self) -> CrdLst:
        """
        Calculates coordinates for all nodes.

        Coordinates take place in the standard x-y-axial coordinate system.
        Each hexagon is composed of 6 coordinates. They follow the @self.moveset
        sequence, meaning:

               ×            (2,1)
            ×     ×    (0,0)     (4,0)
            |     |  =   |         |
            ×     ×    (0,-2)    (4,-2)
               ×            (2,-3)

        From (0,0) you get to (2,1) by applying (+2,+1) or an up-right move.
        From (2,1) you get to (4,0) by applying (+2,-1) or a down-right move, and
        so on.
        """
        r = 0  # starting rotation
        i = 1  # starting node
        sc: Crd = (0, 0)  # starting coordinates
        clst: CrdLst = {i: sc}  # starting position

        for digit in self.bec:
            digit = int(digit)
            for _ in range(digit):
                i += 1
                self.__add_cdt(i, clst, r)
                r = self.__next_rotation(r)
                sc = clst[i]
            # store next starting direction
            r -= 2

        # add missing edges and nodes to the list
        clst = self.__fill_me_up(clst)

        return clst


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
