import sys
import networkx as nx
from networkx import Graph
import matplotlib.pyplot as plt

Crd = tuple[int, int]  # coordinate
Vtx = int  # vertex
CrdLst = dict[Vtx, Crd]  # list of coordinates for every vertex


class CoordinateSystem():
    """
    Dictionary of 'node:coordinate' pairs.
    """

    def __init__(self, bec: str) -> None:
        self.__x = 1
        self.__y = 1
        self.__moveset: list[Crd] = [
            (2 * self.__x, self.__y),    # 1, up-right
            (2 * self.__x, -self.__y),   # 2, down-right
            (0, -2 * self.__y),          # 3, down
            (-2 * self.__x, -self.__y),  # 4, down-left
            (-2 * self.__x, self.__y),   # 5, up-left
            (0, 2 * self.__y),           # 6, up
        ]
        # Check @__fill_me_up for more details
        self.__hn_moveset: list[Crd] = [
            self.__moveset[1],  # down-right
            self.__moveset[2],  # down
            self.__moveset[3],  # down-left
            self.__moveset[5],  # up
        ]
        self.__hn_clst: CrdLst = {}
        self.clst: CrdLst = {}
        self.__calc_coord(bec)

    def __move(self, node: Crd, move: Crd) -> Crd:
        """
        Moves node to new coordinates specified by move (change of x and y)
        """
        return (node[0] + move[0], node[1] + move[1])

    def __add(self,
              node_id: int,
              clst: CrdLst,
              rotation: int,
              p: None | Crd = None) -> None:

        # predecessor
        if p is None:
            p = self.clst[node_id - 1]
        move: Crd = self.__moveset[rotation]
        new_crd: Crd = self.__move(p, move)
        clst[node_id] = new_crd
        return

    # TODO
    def __fill_me_up(self) -> None:
        """
        Fills up the coordinate list with missing edges and vertices

        Parameters:
            `clst`: coordinate list for all nodes
            `hclst`: coordinate list for all horitontal nodes
        ---
        The original list contains only vertices and edges that form the boundary.
        To fill up the system, it has to go through all horizontal nodes (denoted
        as HN) and draws the missing edges. HN's are nodes that can be reached by
        all moves except ur-right or down-left. In other words, they are:

                        ×
            this --> ×     × <-- this
                     |     |
            this --> ×     × <-- this
                        ×

        The algorithm moves through all levels from top left-most coordinate, to
        bottom right-most. E.g.:

                             ×
            from this --> ×     ×
                          |     |

                            ...   ...

                                |     |
                                ×     × <-- to this
                                   ×

        It checks if a neighbouring HN exists in this level (i.e. 4x right). In case
        it does not, but there are still HN's left somewhere in this level, it moves
        to the next HN. This makes sure, that benzenoid systems with gaps are properly
        filled. E.g.:

                             ×     ×                      ×     ×
                start --> 1 --> 2 --> 3 -------------> x --> y --> z --> NULL
                          |     |     |       ...      |     |     |
             next run --> 4     5     6                ×     ×     ×
                       ×     ×     ×     ×         ×      ×     ×
                       |     |     |     |         |      |     |
                               ...                     ...
                               ...                     ...
                               ...                     ...
                          |     |     |     |     |     |     |
                          ×     ×     ×     ×     ×     ×      ×
                       ×     ×     ×     ×     ×     ×      ×     ×
                       |     |     |     |     |     |      |     |
                          ×     ×     ×     ×     ×     ×      ×

        Node 1 has 2 as it's neighbouring HN, so the hexagon is traced and any missing
        edges drawn. Moving onto 2, it's neighbouring HN is 3, so the procedure repeats.
        3 has no neighbouring HN, but the list still contains x, y and z, so it moves to
        x. When it reaches z, there is no neighbouring HN and no HN's left in this level,
        so it moves on to HN 4.
        """
        raise NotImplementedError

    def __next_rotation(self, r: int):
        """
        Gets the next valid rotation, moving to the beginning/end of moveset if necessary.

        The first calculated coordinate will always be done by an up-right move.
        First calculated coordinate after a new digit is read will always be done
        with a move 2 steps back in the moveset. E.g. first move is always up-right:

                            (2,1)           (2,1)
           (0,0) --1-> (0,0)      --2-> (0,0)    (4,0) --3-> ...

        When the additions are consumed (e.g. 1 in BEC contributes to 1 addition), it resets
        back 2 rotations, so that the next edge is added in the correct direction. Rotations
        are periodical, which means that when it goes back from 1st rotation, it ends up at
        the last rotation in the moveset. E.g.:

            Digit: 1, rotations: [0, 1*], resets to 1-2 = -1 = 5

                                (2,1)
                (0,0) --1-> (0,0)

            Digit: 2, rotations: [5, 0, 1*], resets to 1-2 = -1 = 5

                                                      (3,3)
                                (2,2)            (2,2)
                (0,0) --1->           --2->
                                (2,1)            (2,1)
                           (0,0)            (0,0)

            ...
        """
        r += 1
        match r:
            case 6:
                return 0
            case -1:
                return 5
            case _:
                return r

    def __calc_coord(self, bec: str) -> CrdLst:
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
        so on (check @__next_rotation for more details).

        At the same time mark "horizontal nodes" for the purpose of filling up the
        system after coordinates for boundary nodes are calculated (check @__fill_me_up
        for more details).
        """
        r = 0  # starting rotation
        i = 1  # starting node
        sc: Crd = (0, 0)  # starting coordinates
        self.clst: CrdLst = {i: sc}  # starting position
        self.__hn_clst[i] = sc  # horizontal nodes

        for digit in bec:
            digit = int(digit)
            for _ in range(digit):
                i += 1
                print("===========================================================================")
                print(f"digit: {digit}  i: {i}  r: {r}, move: {self.__moveset[r]}")
                self.__add(i, self.clst, r, None)
                print("---------------------------------------------------------------------------")

                if self.__moveset[r] in self.__hn_moveset:  # it found a HN
                    print(f"Found HN: i: {i}")
                    self.__add(i, self.__hn_clst, r, self.clst[i - 1])

                print("---------------------------------------------------------------------------")
                print(f"clst: {self.clst}")
                print(f"clst: {self.__hn_clst}")

                r = self.__next_rotation(r)
                sc = self.clst[i]
            # store next starting direction
            r -= 2

        # add missing edges and nodes to the list
        # clst = self.__fill_me_up(clst, hn_clst)
        print(("HN list of coordinates:"))
        print(self.__hn_clst)
        return self.clst


class Benzy():
    """
    Creates a benzenoid system from a BEC that can be plotted.
    """

    def __init__(self, bec: str) -> None:
        self.bec: str = self.check_bec(bec)
        self.np = sum([int(d) for d in self.bec])  # perimiter nodes
        self.graph: Graph = self.__graph_from_bec()
        self.coordinates: CoordinateSystem = CoordinateSystem(self.bec)

    def draw_bs(self) -> None:
        """
        Plots the benzenoid system.
        """
        nx.draw(
            G=self.graph,
            pos=self.coordinates.clst,
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

    def __graph_from_bec(self) -> Graph:
        """
        Creates a networkx graph.
        """
        g = Graph()
        g.add_edges_from([(i, i + 1) for i in range(1, self.np)])
        g.add_edge(self.np, 1)  # connect the graph
        return g


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
