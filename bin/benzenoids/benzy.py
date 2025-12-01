"""Program for visualizing a benzenoid system."""

import math
import sys
from pprint import pprint
import networkx as nx
import matplotlib.pyplot as plt

Coordinates = tuple[int, int]


class Vertex:

    def __init__(
        self, vx_id: int, coordinates: Coordinates, vx_type: str | None = None
    ) -> None:
        self.id: int = vx_id
        self.type: str | None = vx_type
        self.x: int = coordinates[0]
        self.y: int = coordinates[1]

    def move(self, move_step: Coordinates) -> Coordinates:
        """Moves vertex to new coordinates."""
        return (self.x + move_step[0], self.y + move_step[1])


class Benzy:
    """Creates a benzenoid system from a BEC that can be plotted."""

    x_step = 1
    y_step = 1
    moveset: list[Coordinates] = [
        (2 * x_step, y_step),  # 1, up-right
        (2 * x_step, -y_step),  # 2, down-right
        (0, -2 * y_step),  # 3, down
        (-2 * x_step, -y_step),  # 4, down-left
        (-2 * x_step, y_step),  # 5, up-left
        (0, 2 * y_step),  # 6, up
    ]

    # NOTE: is it really necessary to work with 2 lists of vertices?
    # Just use @self.coordinates and create functions for searching
    # for primary vertices
    primary_vertices: list[Vertex] = []
    vertices: list[Vertex] = []

    def __init__(self, bec: str) -> None:
        self.bec: str = self.check_bec(bec)
        self.perimiter_vertices: int = sum(int(d) for d in self.bec)
        self.graph: nx.Graph = self.graph_from_bec()
        self.calculate_coordinates()
        self.coordinates: list[Coordinates] = self.get_coordinates()

    def graph_from_bec(self) -> nx.Graph:
        """Creates a networkx nx.Graph."""
        g = nx.Graph()
        g.add_edges_from([(i, i + 1) for i in range(1, self.perimiter_vertices)])
        g.add_edge(self.perimiter_vertices, 1)  # connect the nx.Graph
        return g

    def draw_benzenoid_system(self) -> None:
        """Plots the benzenoid system."""
        nx.draw(
            G=self.graph,
            pos={vx.id: (vx.x, vx.y) for vx in self.vertices},  # needs a dict
            with_labels=True,
            node_size=700,
            node_color="skyblue",
            font_weight="bold",
        )
        plt.title(f"Benzenoid system of {self.bec}")
        plt.show()

    def check_bec(self, bec: str) -> str:
        """Makes sure that the provided BEC is valid.

        Valid BEC is composed only of numbers between 1-5.
        """
        for d in bec:
            if not d.isdigit():
                raise ValueError("Illegal boundary edges code. Must be numeric.")
            if int(d) == 6 or int(d) == 0:
                raise ValueError("Illegal boundary edges code. Cannot contain 6 or 0")
        return bec

    def get_vertex_id(self, coordinates: Coordinates, strict=False) -> int | None:
        """Finds vertex with given coordinates."""

        print(f"searching for {coordinates} ... ", end="")
        for vx in self.vertices:
            if (vx.x, vx.y) == coordinates:
                print(f"found vertex {vx.id}", end="\n")
                return vx.id

        print()
        if not strict:
            vx = self.vertices[len(self.vertices) - 1]
            return vx.id + 1  # return next possible vertice id
        else:
            return (math.inf, math.inf)

    def get_vertex(self, coordinates: Coordinates) -> Vertex | None:
        for vx in self.vertices:
            if (vx.x, vx.y) == coordinates:
                return vx
        return None

    def get_coordinates(self) -> list[Coordinates]:
        lst = [(vx.x, vx.y) for vx in self.vertices]
        return lst

    def add_vertex(
        self, new_id: int, rotation: int, predecessor: Vertex | None = None
    ) -> None:
        """Adds new coordinates to system coordinate dictionary."""
        if predecessor is None:
            predecessor = self.vertices[new_id - 1]
        move_step: Coordinates = self.moveset[rotation]
        new_crd: Coordinates = predecessor.move(move_step)
        new_vx: Vertex = Vertex(new_id, new_crd)
        self.vertices.append(new_vx)

    def find_coordinates(self, coordinates: Coordinates) -> bool:
        for vx in self.vertices:
            if coordinates == (vx.x, vx.y):
                return True
        return False

    def find_edge(self, u: Vertex, v: Vertex) -> bool:
        print(f"\nSearching edge for {u.id} and {v.id}... ", end="")
        if self.graph.has_edge(u.id, v.id):
            print("found edge")
            return True
        else:
            return False

    def is_primary(self, vx: Vertex) -> bool:
        """Checks is the given vertex fits the criteria for a primary vertex.

        Primary vertices (denoted as PN) are vertices that fit 3 criteria:
        (1) their x-coordinate is divisible by 2 and
        (2) their y-coordinate is divisible by 3 and
        (3) there is a vertex immeadiatelly below them (i.e. (x,y-2))

                          (2,1)
            this --> (0,0)     (4,0) <-- this
                       |         |
                     (0,-2)    (4,-2)
                          (2,-3)

        """
        return (
            vx.x % 2 == 0 and vx.y % 3 == 0 and self.find_coordinates((vx.x, vx.y - 2))
        )

    def is_inner_primary(self, vx: Vertex) -> bool:
        move_step: Coordinates = (-2 * self.x_step, self.y_step)
        return self.find_coordinates(vx.move(move_step))

    def sort_primary_vertices(self) -> None:
        """Sort PN coordinates descending by y and ascending by x."""
        n = len(self.primary_vertices)
        for i in range(n):
            for j in range(i + 1, n):
                # descending by y, when y are different
                if self.primary_vertices[i].y < self.primary_vertices[j].y:
                    tmp = self.primary_vertices[i]
                    self.primary_vertices[i] = self.primary_vertices[j]
                    self.primary_vertices[j] = tmp
                # ascending by x, when y are the same
                elif self.primary_vertices[i].y == self.primary_vertices[j].y:
                    if self.primary_vertices[i].x > self.primary_vertices[j].x:
                        tmp = self.primary_vertices[i]
                        self.primary_vertices[i] = self.primary_vertices[j]
                        self.primary_vertices[j] = tmp

    def next_rotation(self, rotation: int):
        """Gets the next valid rotation, moving to the beginning/end of moveset if necessary.

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

    def trace_hexagon(self, start_vx: Vertex) -> None:
        print(f"\nTracing from {start_vx.id}")

        rotation = 0
        cur_vx: Vertex = start_vx

        for _ in range(6):
            next_coordinates: Coordinates = cur_vx.move(self.moveset[rotation])
            next_id: int = self.get_vertex_id(next_coordinates)
            next_vx: Vertex = Vertex(next_id, next_coordinates)

            if self.find_coordinates(next_coordinates):
                if not self.find_edge(cur_vx, next_vx):
                    print(f"* adding edge: {cur_vx.id, next_vx.id}")
                    self.graph.add_edge(cur_vx.id, next_vx.id)
            else:
                # create new vertex and new edge
                print(f"* creating new vertex for {next_vx.id} {next_coordinates}")
                self.graph.add_node(next_id)
                self.add_vertex(next_vx, rotation, cur_vx)
                print(f"* adding edge: {(cur_vx.id, next_vx.id)}")
                self.graph.add_edge(cur_vx.id, next_vx.id)

                if self.is_inner_primary(next_vx):
                    self.primary_vertices.insert(0, next_vx)
                    self.sort_primary_vertices()  # is this needed?

            cur_vx = next_vx
            rotation = self.next_rotation(rotation)

    # BUG: for example 3233321112523242211122
    def fill_me_up(self) -> None:
        """Fills up the coordinate list with missing edges and vertices
        ---
        The original list contains only vertices and edges that form the boundary.
        To fill up the system, it has to go through all primary vertices (check
        @__is_primary for details) and draws the missing edges.

        The algorithm moves through all levels from top left-most to bottom right-most
        primary vertex. E.g.:

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

        Vertex 1 has 2 as it's neighbouring PN, so the hexagon is traced and any missing
        edges drawn. Moving onto 2, it's neighbouring PN is 3, so the procedure repeats.
        3 has no neighbouring PN, but the list still contains x, y and z, so it moves to
        x. When it reaches z, there is no neighbouring PN and no PN's left in this level,
        so it moves on to PN 4.

        Vertex type is important for determining if boundary primary vertices should be traced.
        If it's between immeadiate left and right types, it should, otherwise not. E.g.:

                   ×           ×
                1     2     3     4
                |     |     |     |
                ×     ×     ×     ×
                   ×     ×     ×
                      ...  ...  ...

        """
        print("\nAll Vertices:")
        [print(n.id, (n.x, n.y)) for n in self.vertices]

        self.sort_primary_vertices()
        print("\nSorted Primary Vertices:")
        [print(n.id, (n.x, n.y)) for n in self.primary_vertices]

        while self.primary_vertices is not []:
            # 1. get vertex from list of primary vertices
            current_vx: Vertex = self.primary_vertices.pop(0)

            # 2. does a next PN exist in this level?
            try:
                # exception will happen here
                next_vx: Vertex = self.primary_vertices[0]
                print(f"\nNext PN: {next_vx.id} {(next_vx.x, next_vx.y)}")

                if current_vx.y == next_vx.y:
                    print(f"PN exists in level, starting trace for {current_vx.id}")
                    self.trace_hexagon(current_vx)  # trace the hexagon and continue
                else:
                    print("PN doesn't exists in level, moving to next level")
            except IndexError:
                print("\nNo more primary vertices")
                break

    def calculate_coordinates(self) -> None:
        """Calculates coordinates for all vertices.

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

        At the same time mark "primary" vertices" for the purpose of filling up the
        system after coordinates for boundary vertices are calculated (check @__fill_me_up
        for more details).
        """
        rotation = 0  # starting rotation
        id = 1
        cur_vx = Vertex(id, (0, 0))  # starting vertex
        self.vertices.append(cur_vx)  # starting position

        for digit in self.bec:
            digit = int(digit)
            for _ in range(digit):
                id += 1

                print(
                    f"digit: {digit}, vx id: {id}, rotation: {
                      rotation}, move: {self.moveset[rotation]}"
                )

                # add next vertex to list based on rotation
                next_coordinates = cur_vx.move(self.moveset[rotation])
                cur_vx = Vertex(id, next_coordinates)
                self.vertices.append(cur_vx)

                rotation = self.next_rotation(rotation)
            rotation -= 2  # store next starting direction

        # pop the last coordinate (it shadows the first vertex)
        self.vertices.pop(-1)

        # traverse the coordinates again and find primary vertices on the boundary
        for vx in self.vertices:
            if self.is_primary(vx):
                self.primary_vertices.append(vx)

        # add missing edges and vertices to the list
        self.fill_me_up()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: benzy.py [BEC | list BEC]")
        print("Examples:", end=" ")
        for e in ["55", "2525", "333333", "4445312351231", "323232323232"]:
            print(e, end=" ")
        print()

    # for b in sys.argv[1:]:
    #     bs = Benzy(b)
    #     bs.draw_benzenoid_system()

    bs = Benzy("3233321112523242211122")
    bs.draw_benzenoid_system()
