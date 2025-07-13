import math
from typing import List, Set, Tuple
from constants import HEX_SIZE, Port
from edge import Edge


class Vertex:
    def __init__(self, coordinate: Tuple[float, float]):
        self.coordinate = coordinate
        self.neighbors: Set[Vertex] = set()
        self.name = ""
        self.tile_association: List["Tile"] = []  # type: ignore # noqa: F821
        self.port = None
        self.settlement = None

    def __eq__(self, other):
        if not isinstance(other, Vertex):
            return False
        return self.coordinate == other.coordinate

    def __hash__(self):
        return hash(self.coordinate)

    def find_all_neighbors(
        self, set_of_other_vertices: Set["Vertex"], list_of_edges: List[Edge]
    ) -> None:
        """
        For generating all edges to neighboring vertices
        """
        epsilon = 1
        for vertice in set_of_other_vertices:
            distance = math.sqrt(
                (vertice.coordinate[0] - self.coordinate[0]) ** 2
                + (vertice.coordinate[1] - self.coordinate[1]) ** 2
            )

            if distance - HEX_SIZE < epsilon and distance != 0:
                self.neighbors.add(vertice)

                Edge.generate_new_edge((vertice, self), list_of_edges)

    def label_vertex(self, i: int) -> None:
        """
        For setting vertex name and a port if there is one
        """
        self.name = f"v{i}"
        self.port = Port.get_port(i)

    def add_tile_association(self, points, Tile: "Tile") -> None:  # type: ignore # noqa: F821
        """
        Get all tiles the vertex is associated with
        """
        for point in points:
            if self.coordinate == point:
                self.tile_association.append(Tile)

    def build_settlement(self, player) -> None:
        self.settlement = player

    def check_if_can_build_settlement(self) -> None:
        # If vertex already has a settlement then you cannot build another
        if self.settlement:
            return False

        # If vertex neighbor has a settlement you also can't build a settlement
        for vertex in self.neighbors:
            if vertex.settlement:
                return False

        return True
