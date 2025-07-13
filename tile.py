import math
from typing import Set
from constants import DICE_SUM_PROBABILITY, HEX_SIZE, Color
from vertex import Vertex


class Tile:
    def __init__(
        self,
        resource: str,
        q: int,
        r: int,
        number: int,
        set_of_vertices: Set[Vertex],
    ):
        self.resource = resource
        self.number = number
        self.color = Color.resource_to_color(resource)
        self.x, self.y = self.hex_to_pixel(q, r)

        self.points = [
            (
                round(self.x + HEX_SIZE * math.sin(math.radians(60 * i)), 0),
                round(self.y + HEX_SIZE * math.cos(math.radians(60 * i)), 0),
            )
            for i in range(6)
        ]

        for point in self.points:
            set_of_vertices.add(Vertex(point))

        for vertex in set_of_vertices:
            vertex.add_tile_association(self.points, self)

    # Only used once at the start to get the (x, y) of the center and the vertices for the graph
    def hex_to_pixel(self, q: int, r: int):
        x = HEX_SIZE * (math.sqrt(3) / 2 * q + math.sqrt(3) * r)
        y = HEX_SIZE * (3 / 2 * q)
        return x, y

    def tile_num_to_prob(self) -> float:
        return DICE_SUM_PROBABILITY[self.number]
