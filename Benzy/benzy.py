import sys
from pprint import pprint
from networkx import Graph
import networkx as nx
import matplotlib.pyplot as plt

Coordinates = tuple[int, int]
Vertex = int
CoordinateList = dict[Vertex, Coordinates]


class Benzy():
    """ Creates a benzenoid system from a BEC that can be plotted. """
    x_step = 1
    y_step = 1
    moveset: list[Coordinates] = [
        (2 * x_step, y_step),    # 1, up-right
        (2 * x_step, -y_step),   # 2, down-right
        (0, -2 * y_step),        # 3, down
        (-2 * x_step, -y_step),  # 4, down-left
        (-2 * x_step, y_step),   # 5, up-left
        (0, 2 * y_step),         # 6, up
    ]

    def __init__(self, bec: str) -> None:
        self.bec: str = self.check_bec(bec)
        self.perimiter_nodes: int = sum(int(d) for d in self.bec)
        self.graph: Graph = self.graph_from_bec()
        self.primary_coordinates: CoordinateList = {}
        self.coordinates: CoordinateList = {}
        self.calculate_coordinates()

    def graph_from_bec(self) -> Graph:
        """ Creates a networkx graph.  """
        g = Graph()
        g.add_edges_from([(i, i + 1) for i in range(1, self.perimiter_nodes)])
        g.add_edge(self.perimiter_nodes, 1)  # connect the graph
        return g

    def draw_benzenoid_system(self) -> None:
        """ Plots the benzenoid system.  """
        nx.draw(
            G=self.graph,
            pos=self.coordinates,
            with_labels=False,
            node_size=0,
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

    def get_node(self, coordinates: Coordinates) -> Vertex:
        for node in self.coordinates.items():
            if node[1] == coordinates:
                return node[0]
        return -1  # hmm

    def move(self, node: Coordinates, move: Coordinates) -> Coordinates:
        """ Moves node to new coordinates specified by move (change of x and y) """
        return (node[0] + move[0], node[1] + move[1])

    def add_coordinate(self,
                       node_id: Vertex,
                       rotation: int,
                       predecessor: None | Coordinates = None) -> None:
        """ Adds new coordinate to coordinate list, based on previous node and move step.  """
        if predecessor is None:  # predecessor
            predecessor = self.coordinates[node_id - 1]
        move: Coordinates = self.moveset[rotation]
        new_crd: Coordinates = self.move(predecessor, move)
        self.coordinates[node_id] = new_crd

    def add_node(self, node: Vertex) -> None:
        self.graph.add_node(node)

    def add_edge(self, u: Vertex, v: Vertex) -> None:
        self.graph.add_edge(u, v)

    def find_coordinate(self, node: Coordinates) -> bool:
        return node in self.coordinates.values()

    def find_edge(self, u: Vertex, v: Vertex) -> bool:
        return (u, v) in self.graph.edges()

    def is_primary(self, node: Coordinates) -> bool:
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
        return node[0] % 2 == 0 and node[1] % 3 == 0 and self.find_coordinate((node[0], node[1] - 2))

    def sort_primary_nodes(self) -> tuple[list[Vertex], list[Coordinates]]:
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
        for node_id in sorted_ids:
            sorted_coordinates.append(self.primary_coordinates[node_id])

        return sorted_ids, sorted_coordinates

    def trace_hexagon(self, start_node: tuple[Vertex, Coordinates]) -> None:
        rotation = 0
        print("= trace hexagon ================================================")
        print(f"tracing from {start_node}")
        for _ in range(6):
            next_coordinates: Coordinates = self.move(start_node[1], self.moveset[rotation])
            next_node: Vertex = self.get_node(next_coordinates)

            if self.find_coordinate(next_coordinates):
                if not self.find_edge(start_node[0], next_node):
                    print("----------------------------------------------------------------")
                    print(f"adding edge: {(start_node[0], next_node)}")
                    self.add_edge(start_node[0], next_node)
            else:
                # create new node and new edge
                print("----------------------------------------------------------------")
                print(f"creating new node edge: {next_node}, {next_coordinates}")
                self.add_node(next_node)
                self.add_coordinate(next_node, rotation, start_node[1])
                print(f"adding edge: {(start_node[0], next_node)}")
                self.add_edge(start_node[0], next_node)

            start_node = (next_node, next_coordinates)
            rotation = self.next_rotation(rotation)

    def fill_me_up(self) -> None:
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
        sorted_ids, sorted_coordinates = self.sort_primary_nodes()
        print("= fill me up ===================================================")
        print("sorted PNs")
        _ = [print(sorted_ids[i], sorted_coordinates[i]) for i in range(len(sorted_ids))]

        for i in range(len(self.primary_coordinates)):
            # 1. get node from list of primary nodes
            current_node: tuple[Vertex, Coordinates] = (sorted_ids[i], sorted_coordinates[i])
            print("= fill me up - inner loop=======================================")
            print(f"at PN {current_node}")
            try:
                next_primary_node: tuple[Vertex, Coordinates] = (
                    sorted_ids[i + 1], sorted_coordinates[i + 1]
                )
                # 2. does a next PN exist in this level?
                if current_node[1][1] == next_primary_node[1][1]:
                    print("PN exists in level, starting trace")
                    self.trace_hexagon(current_node)  # trace the hexagon and continue
                else:
                    print("PN doesn't exists in level, moving to next level")
            except IndexError:  # no more primary nodes
                print("no more primary nodes")
                break

    def next_rotation(self, rotation: int):
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

    def calculate_coordinates(self) -> None:
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
                      rotation}, move: {self.moveset[rotation]}")

                self.add_coordinate(node_id, rotation, None)

                rotation = self.next_rotation(rotation)
            rotation -= 2  # store next starting direction

        # pop the last coordinate (it shadows the first node)
        self.coordinates.pop(len(self.coordinates))

        # traverse the coordinates again and find primary nodes on the boundary
        print("===========================================================================")
        print("Coordinates:")
        pprint(self.coordinates)

        for node_id, coordinates in self.coordinates.items():
            if self.is_primary(coordinates):
                print(f"Found PN: {node_id}")
                self.primary_coordinates[node_id] = coordinates

        # add missing edges and nodes to the list
        self.fill_me_up()

        print("---------------------------------------------------------------------------")
        print("PN coordinates:")
        pprint(self.primary_coordinates)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: benzy.py [BEC | list BEC]""")
        print("Examples:", end=" ")
        for e in ["55", "2525", "333333", "444" "5312351231"]:
            print(e, end=" ")
        print()

    for b in sys.argv[1:]:
        bs = Benzy(b)
        bs.draw_benzenoid_system()
