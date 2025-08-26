from __future__ import annotations
import math
import random
from typing import List, Optional, Set, Tuple
import pygame
from constants import (
    NUMBER_DICT,
    OFFSET_Q,
    OFFSET_R,
    RESOURCE_DICT,
    Color,
    Resource,
)
from player import Player
from tile import Tile
from vertex import Vertex
from edge import Edge


class Board:
    def __init__(self, screen):
        self.vertices: List[Vertex] = []
        self.edges: List[Edge] = []
        self.tiles: List[Tile] = []
        self.screen: pygame.Surface = screen
        self.generate_new_board()

    @staticmethod
    def get_random_resource_order() -> List[str]:
        result: List[str] = []
        for value, count in RESOURCE_DICT.items():
            result.extend([value] * count)
        random.shuffle(result)
        return result

    @staticmethod
    def get_random_number_order() -> List[int]:
        result: List[int] = []
        for value, count in NUMBER_DICT.items():
            result.extend([value] * count)
        random.shuffle(result)
        return result

    def generate_new_board(self) -> None:
        # Get random number and tile order
        while True:
            resource_order = self.get_random_resource_order()
            desert_index = resource_order.index(Resource.DESERT.value)
            number_order = self.get_random_number_order()
            number_order.insert(desert_index, -1)

            index = 0
            set_of_vertices: Set[Vertex] = set()
            self.screen.fill(Color.BACKGROUND.to_rgb())  # Light gray background
            grid = {}
            # q is straight across (basically x)
            # r is angled down (disturbed y)
            for q in range(0, 5):
                for r in range(0, 5):
                    if not (q + r < 2 or q + r > 6):
                        grid[(q, r)] = 1

            for (q, r), _ in grid.items():
                new_tile = Tile(
                    resource_order[index],
                    q + OFFSET_Q,
                    r + OFFSET_R,
                    number_order[index],
                    set_of_vertices,
                )
                self.tiles.append(new_tile)
                index += 1

            self.vertices = list(set_of_vertices)

            if self.is_board_legal():
                break

        # Get all edges by looping through vertices
        for vertex in self.vertices:
            vertex.find_all_neighbors(self.vertices, self.edges)

        self.vertices: List[Vertex] = sorted(
            self.vertices,
            key=lambda obj: (obj.coordinate[1], obj.coordinate[0]),
        )
        # Label vertices and ports
        i: int = 1
        for vertex in self.vertices:
            vertex.label_vertex(i)
            i += 1

        # Check to see if ports are working
        self.display_board()

    def display_board(self) -> None:
        # For showing tiles
        font = pygame.font.Font(None, 36)
        for tile in self.tiles:
            pygame.draw.polygon(self.screen, tile.color, tile.points)

            if tile.number != -1:
                text_surface = font.render(
                    str(tile.number), True, Color.OUTLINE.to_rgb()
                )  # Create text surface
                text_rect = text_surface.get_rect(
                    center=(tile.x, tile.y)
                )  # Center the rectangle
                self.screen.blit(
                    text_surface, text_rect.topleft
                )  # Draw text at adjusted position

        # For showing edges
        for edge in self.edges:
            pygame.draw.line(
                self.screen,
                Color.EDGE.to_rgb(),
                edge.vertex_set[0].coordinate,
                edge.vertex_set[1].coordinate,
                10,
            )

        # For showing vertices
        font = pygame.font.Font(None, 24)
        for vertex in self.get_list_of_settleable_vertices():
            pygame.draw.circle(self.screen, Color.VERTEX.to_rgb(), vertex.coordinate, 5)

        pygame.display.flip()

    def check_collision(self, click_position: Tuple[int, int]) -> Optional[Tile]:
        # Return tile if it collides with the click
        for tile in self.tiles:
            if pygame.draw.polygon(
                self.screen, tile.color, tile.points, 0
            ).collidepoint(click_position):
                return tile

        # Return None if no collision
        return None

    def check_if_vertex_collision(
        self, click_position: Tuple[int, int]
    ) -> Optional[Vertex]:
        mx, my = click_position
        threshold = 10
        for vertex in self.vertices:
            distance = math.sqrt(
                (mx - vertex.coordinate[0]) ** 2 + (my - vertex.coordinate[1]) ** 2
            )

            if distance <= threshold and vertex.check_if_can_build_settlement():
                return vertex

        return None

    def create_settlement(self, vertex: Vertex, player: Player) -> None:
        vertex.build_settlement(player)

        # Draw settlement
        width, height = 28, 21
        x, y = vertex.coordinate[0] - width // 2, vertex.coordinate[1] - height // 2

        roof_points = [
            (x, y),
            (x + width // 2, y - height // 2),
            (x + width, y),
        ]

        pygame.draw.rect(self.screen, player.color, (x, y, width, height))
        pygame.draw.polygon(self.screen, player.color, roof_points)

        pygame.display.flip()

    def check_if_edge_collision(
        self,
        click_position: Tuple[int, int],
        player: Player,
        game_phase: int,
        current_vertex: Optional[Vertex] = None,
    ) -> Optional[Edge]:
        mx, my = click_position
        threshold = 10
        for edge in self.edges:
            distance = math.sqrt(
                (
                    mx
                    - (
                        edge.vertex_set[0].coordinate[0]
                        + edge.vertex_set[1].coordinate[0]
                    )
                    / 2
                )
                ** 2
                + (
                    my
                    - (
                        edge.vertex_set[0].coordinate[1]
                        + edge.vertex_set[1].coordinate[1]
                    )
                    / 2
                )
                ** 2
            )

            if distance <= threshold and edge.check_if_can_build_road(
                self.edges, player, game_phase, current_vertex
            ):
                return edge

        return None

    def create_road(self, edge: Edge, player: Player) -> None:
        edge.build_road(player)

        pygame.draw.line(
            self.screen,
            player.color,
            edge.vertex_set[0].coordinate,
            edge.vertex_set[1].coordinate,
            10,
        )

        pygame.display.flip()

    def is_board_legal(self) -> bool:
        for vertex in self.vertices:
            counter_6_8 = 0
            counter_2_12 = 0
            for tile in vertex.tile_association:
                if tile.number in [6, 8]:
                    counter_6_8 += 1
                if tile.number in [2, 12]:
                    counter_2_12 += 1
            if counter_6_8 > 1 or counter_2_12 > 1:
                return False

        return True

    def get_list_of_settleable_vertices(self) -> List[Vertex]:
        list_of_vertices: List[Vertex] = []
        for vertex in self.vertices:
            if vertex.settlement is None and all(
                vertex_neighbors.settlement is None
                for vertex_neighbors in vertex.neighbors
            ):
                list_of_vertices.append(vertex)

        return list_of_vertices

    def get_list_of_edges_off_vertex(self, vertex) -> List[Edge]:
        list_of_edges: List[Edge] = []
        for edge in self.edges:
            if not edge.road and (
                edge.vertex_set[0] == vertex or edge.vertex_set[1] == vertex
            ):
                list_of_edges.append(edge)

        return list_of_edges

    def redraw_settleable_vertices(self) -> None:
        for vertex in self.vertices:
            if not vertex.settlement:
                pygame.draw.circle(
                    self.screen, Color.EDGE.to_rgb(), vertex.coordinate, 5
                )

        for vertex in self.get_list_of_settleable_vertices():
            pygame.draw.circle(self.screen, Color.VERTEX.to_rgb(), vertex.coordinate, 5)

        pygame.display.flip()
