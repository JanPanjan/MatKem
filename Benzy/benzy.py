import sys
from pprint import pprint
import networkx as nx
from networkx import Graph
import matplotlib.pyplot as plt

Coordinates = tuple[int, int]  # coordinate
Vertex = int  # vertex
CoordinateList = dict[Vertex, Coordinates]


class CoordinateSystem():
    """
    Dictionary of 'node:coordinate' pairs.
    """

    def __init__(self, bec: str) -> None:
        self.__x = 1
        self.__y = 1
        self.__moveset: list[Coordinates] = [
            (2 * self.__x, self.__y),    # 1, up-right
            (2 * self.__x, -self.__y),   # 2, down-right
            (0, -2 * self.__y),          # 3, down
            (-2 * self.__x, -self.__y),  # 4, down-left
            (-2 * self.__x, self.__y),   # 5, up-left
            (0, 2 * self.__y),           # 6, up
        ]
        self.__primary_coordinates: CoordinateList = {}  # primary nodes
        self.coordinates: CoordinateList = {}
        self.__calculate_coordinates(bec)

    def __move(self, node: Coordinates, move: Coordinates) -> Coordinates:
        """ Moves node to new coordinates specified by move (change of x and y) """
        return (node[0] + move[0], node[1] + move[1])

    def __add(self, node_id: int, node_crd: Coordinates, clst: CoordinateList) -> None:
        """ Adds new coordinate to coordinate list.  """
        clst[node_id] = node_crd

    def __add_from_coordinates(self,
                               node_id: int,
                               coordinates: CoordinateList,
                               rotation: int,
                               predecessor: None | Coordinates = None) -> None:
        """ Adds new coordinate to coordinate list, based on previous node and move step.  """
        if predecessor is None:  # predecessor
            predecessor = self.coordinates[node_id - 1]
        move: Coordinates = self.__moveset[rotation]
        new_crd: Coordinates = self.__move(predecessor, move)
        coordinates[node_id] = new_crd
        return

    def __is_primary(self, node: Coordinates) -> bool:
        """ Checks is the given node fits the criteria for a primary node.

        Primary nodes (denoted as PN) are nodes that fit 3 criteria:
        (1) their x-coordinate is divisible by 2 and
        (2) their y-coordinate is divisible by 3 and
        (3) there is a node immeadiatelly below them (i.e. (x,y-2))

                          (2,1)
            this --> (0,0)     (4,0) <-- this
                       |         |
                     (0,-2)    (4,-2)
                          (2,-3)

        """
        raise NotImplementedError

        # TODO
    def __fill_me_up(self) -> None:
        """ Fills up the coordinate list with missing edges and vertices

        Parameters:
            `clst`: coordinate list for all nodes
            `hclst`: coordinate list for all primary nodes
        ---
        The original list contains only vertices and edges that form the boundary.
        To fill up the system, it has to go through all primary nodes (check
        @__is_primary for details) and draws the missing edges.

        The algorithm moves through all levels from top left-most to bottom right-most
        primary node. E.g.:

                             ×
            from this --> ×     ×
                          |     |
                            ...   ...
                                ×     × <-- to this
                                |     |
                                ×     ×
                                   ×

        It checks if a neighbouring PN exists in this level (i.e. 4x right). In case
        it does not, but there are still PN's left somewhere in this level, it moves
        to the next PN. This makes sure, that benzenoid systems with gaps are properly
        filled. E.g.:

                             ×     ×                      ×     ×
                start --> 1 --> 2 --> 3 -------------> x --> y --> z --> NULL
                          |     |     |       ...      |     |     |
                          ×     ×     ×                ×     ×     ×
          next run --> 4     5     6     7         ×      ×     ×
                       |     |     |     |         |      |     |
                               ...                     ...
                               ...                     ...
                               ...                     ...
                          |     |     |     |     |     |     |
                          ×     ×     ×     ×     ×     ×      ×
                       ×     ×     ×     ×     ×     ×      ×     ×
                       |     |     |     |     |     |      |     |
                       ×     ×     ×     ×     ×     ×      ×     ×
                          ×     ×     ×     ×     ×     ×      ×

        Node 1 has 2 as it's neighbouring PN, so the hexagon is traced and any missing
        edges drawn. Moving onto 2, it's neighbouring PN is 3, so the procedure repeats.
        3 has no neighbouring PN, but the list still contains x, y and z, so it moves to
        x. When it reaches z, there is no neighbouring PN and no PN's left in this level,
        so it moves on to PN 4.
        """
        raise NotImplementedError

    def __next_rotation(self, rotation: int):
        """ Gets the next valid rotation, moving to the beginning/end of moveset if necessary.

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
        rotation += 1
        match rotation:
            case 6:
                return 0
            case -1:
                return 5
            case _:
                return rotation

    # BUG: detecting PN's is not correct
    def __calculate_coordinates(self, bec: str) -> CoordinateList:
        """ Calculates coordinates for all nodes.

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

        At the same time mark "primary" nodes" for the purpose of filling up the
        system after coordinates for boundary nodes are calculated (check @__fill_me_up
        for more details).
        """
        rotation = 0  # starting rotation
        node_id = 1  # starting node
        start_coordinates: Coordinates = (0, 0)  # starting coordinates
        self.coordinates: CoordinateList = {node_id: start_coordinates}  # starting position
        self.__primary_coordinates[node_id] = start_coordinates  # primary nodes

        for digit in bec:
            digit = int(digit)
            for _ in range(digit):
                node_id += 1
                print("===========================================================================")
                print(f"digit: {digit}  node id: {node_id}  rotation: {
                      rotation}, move: {self.__moveset[rotation]}")

                self.__add_from_coordinates(node_id, self.coordinates, rotation, None)

                # print("---------------------------------------------------------------------------")

                # BUG: fix this PN detection
                if self.__is_primary(self.coordinates[node_id]):
                    # print(f"Found PN: i: {i}")
                    self.__add_from_coordinates(
                        node_id, self.__primary_coordinates, rotation, self.coordinates[node_id - 1])

                # print("---------------------------------------------------------------------------")
                # print(f"clst: {self.coordinates}")
                # print(f"clst: {self.__primary_coordinates}")

                rotation = self.__next_rotation(rotation)
                start_coordinates = self.coordinates[node_id]
            # store next starting direction
            rotation -= 2

        # add missing edges and nodes to the list
        # clst = self.__fill_me_up(clst, pn_clst)
        print(("pN list of coordinates:"))
        pprint(self.__primary_coordinates)
        return self.coordinates


class Benzy():
    """
    Creates a benzenoid system from a BEC that can be plotted.
    """

    def __init__(self, bec: str) -> None:
        self.bec: str = self.check_bec(bec)
        self.perimiter_nodes = sum([int(d) for d in self.bec])  # perimiter nodes
        self.graph: Graph = self.__graph_from_bec()
        self.coordinates: CoordinateSystem = CoordinateSystem(self.bec)

    def draw_bs(self) -> None:
        """ Plots the benzenoid system.  """
        nx.draw(
            G=self.graph,
            pos=self.coordinates.coordinates,
            with_labels=True,
            node_size=700,
            node_color="skyblue",
            font_weight="bold"
        )
        plt.title(f"Benzenoid system of {self.bec}")
        plt.show()

    def check_bec(self, bec: str) -> str:
        """ Makes sure that the provided BEC is valid.

        Valid BEC is composed only of numbers between 1-5.
        """
        for d in bec:
            if not d.isdigit():
                raise ValueError("Illegal boundary edges code. Must be numeric.")
            if int(d) == 6 or int(d) == 0:
                raise ValueError("Illegal boundary edges code. Cannot contain 6 or 0")
        return bec

    def __graph_from_bec(self) -> Graph:
        """ Creates a networkx graph.  """
        g = Graph()
        g.add_edges_from([(i, i + 1) for i in range(1, self.perimiter_nodes)])
        g.add_edge(self.perimiter_nodes, 1)  # connect the graph
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
