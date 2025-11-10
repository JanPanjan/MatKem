import sys
import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint
from networkx import Graph

Coordinates = tuple[int, int]
Vertex = int
CoordinateList = dict[Vertex, Coordinates]


class CoordinateSystem():
    """ Dictionary of 'node:coordinate' pairs. """

    def __init__(self, bec: str) -> None:
        self.bec = bec
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
        self.primary_coordinates: CoordinateList = {}
        self.coordinates: CoordinateList = {}
        self.__calculate_coordinates()

    def __move(self, node: Coordinates, move: Coordinates) -> Coordinates:
        """ Moves node to new coordinates specified by move (change of x and y) """
        return (node[0] + move[0], node[1] + move[1])

    def __add(self, id: Vertex, coordinates: Coordinates) -> None:
        """ Adds new coordinate to coordinate list.  """
        self.coordinates[id] = coordinates

    def __add_from_coordinates(self,
                               node_id: Vertex,
                               rotation: int,
                               predecessor: None | Coordinates = None) -> None:
        """ Adds new coordinate to coordinate list, based on previous node and move step.  """
        if predecessor is None:  # predecessor
            predecessor = self.coordinates[node_id - 1]
        move: Coordinates = self.__moveset[rotation]
        new_crd: Coordinates = self.__move(predecessor, move)
        self.coordinates[node_id] = new_crd
        return

    def __find(self, node: Coordinates) -> bool:
        return node in self.coordinates.values()

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
        return node[0] % 2 == 0 and node[1] % 3 == 0 and self.__find((node[0], node[1] - 2))

        # TODO

    def __sort_primary_nodes(self) -> tuple[list[Vertex], list[Coordinates]]:
        """ Sort PN coordinates descending by y and ascending by x.

        Returns two lists, one of sorted node ids and one of sorted node coordinates.
        """
        sorted_ids: list[Vertex]
        sorted_coordinates: list[Coordinates] = []

        sorted_ids = sorted(
            self.primary_coordinates,
            key=lambda key: (
                -self.primary_coordinates[key][1],
                self.primary_coordinates[key][0]
            ),
            reverse=False
        )
        [sorted_coordinates.append(self.primary_coordinates[sorted_ids[i]])
         for i in range(len(sorted_ids))]

        return sorted_ids, sorted_coordinates

    def __fill_me_up(self) -> None:
        """ Fills up the coordinate list with missing edges and vertices
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
        sorted_ids, sorted_coordinates = self.__sort_primary_nodes()
        print("----------------------------------------------------------------")
        print("sorted PNs")
        [print(sorted_ids[i], sorted_coordinates[i]) for i in range(len(sorted_ids))]

        # trace the hexagons PN's define and add any missing nodes/edges
        # 1. it always starts with a primary node with at least one neighbour, so we trace immeadiatelly
        # 2. checks if next primary node exists in this level
        """
        rotation = 0
        current_node: tuple[Vertex, Coordinates] = (sorted_ids[0], sorted_coordinates[0])
        for i in range(pn):
            self.__trace_hexagon(current_node)

            try:
                next_primary_node: tuple[Vertex, Coordinates] = (sorted_ids[i+1], sorted_coordinates[i+1]) # exception will happen here
                # is it a neighbouring PN (x2==x1+4?)
                if current_node[1][0] != next_primary_node[1][0] + 4:
                    # is it in this level or not (y1==y2?)
                    if current_node[1][1] == next_primary_node[1][1]:
                        pass
            except IndexError: # end of list, no more hexagons to add
                break
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

    def __calculate_coordinates(self) -> None:
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
        node_id: Vertex = 1  # starting node
        self.coordinates = {node_id: (0, 0)}  # starting position
        self.primary_coordinates = {node_id: (0, 0)}  # primary nodes

        for digit in self.bec:
            digit = int(digit)
            for _ in range(digit):
                node_id += 1
                print(f"digit: {digit}  node id: {node_id}  rotation: {
                      rotation}, move: {self.__moveset[rotation]}")

                self.__add_from_coordinates(node_id, rotation, None)

                rotation = self.__next_rotation(rotation)
            rotation -= 2  # store next starting direction

        # pop the last coordinate (it shadows the first node)
        self.coordinates.pop(len(self.coordinates))

        # traverse the coordinates again and find primary nodes on the boundary
        print("===========================================================================")
        print("Coordinates:")
        pprint(self.coordinates)

        for id, coordinates in self.coordinates.items():
            if self.__is_primary(coordinates):
                print(f"Found PN: {id}")
                self.primary_coordinates[id] = coordinates

        # add missing edges and nodes to the list
        self.__fill_me_up()

        print("---------------------------------------------------------------------------")
        print("PN coordinates:")
        pprint(self.primary_coordinates)
        return


class Benzy():
    """ Creates a benzenoid system from a BEC that can be plotted. """

    def __init__(self, bec: str) -> None:
        self.bec: str = self.check_bec(bec)
        self.perimiter_nodes = sum([int(d) for d in self.bec])
        self.graph: Graph = self.__graph_from_bec()
        self.coordinates: CoordinateSystem = CoordinateSystem(self.bec)

    def __graph_from_bec(self) -> Graph:
        """ Creates a networkx graph.  """
        g = Graph()
        g.add_edges_from([(i, i + 1) for i in range(1, self.perimiter_nodes)])
        g.add_edge(self.perimiter_nodes, 1)  # connect the graph
        return g

    def draw_benzenoid_system(self) -> None:
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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: benzy.py [int | list[int]]""")
        print("Examples:", end=" ")
        for e in ["55", "2525", "333333", "444" "5312351231"]:
            print(e, end=" ")
        print()

    for b in sys.argv[1:]:
        g = Benzy(b)
        g.draw_benzenoid_system()
