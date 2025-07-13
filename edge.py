from __future__ import annotations
from typing import List, Tuple
from constants import GamePhase
from player import Player


class Edge:
    def __init__(self, vertex_set: Tuple["Vertex", "Vertex"]):  # type: ignore  # noqa: F821
        self.vertex_set: Tuple["Vertex"] = vertex_set  # type: ignore  # noqa: F821
        self.road = None

    @classmethod
    def generate_new_edge(
        cls,
        vertex_set: Tuple["Vertex", "Vertex"],  # type: ignore  # noqa: F821
        list_of_edges: List["Edge"],
    ) -> None:
        repeat = False
        for edge in list_of_edges:
            if (
                vertex_set[0].coordinate == edge.vertex_set[0].coordinate
                and vertex_set[1].coordinate == edge.vertex_set[1].coordinate
            ) or (
                vertex_set[1].coordinate == edge.vertex_set[0].coordinate
                and vertex_set[0].coordinate == edge.vertex_set[1].coordinate
            ):
                repeat = True
                break

        if not repeat:
            list_of_edges.append(cls(vertex_set))

    def build_road(self, player) -> None:
        self.road = player

    def check_if_can_build_road(
        self,
        edges: List[Edge],
        player: Player,
        game_phase: int,
        current_vertex: "Vertex",  # type: ignore  # noqa: F821
    ) -> None:
        if game_phase == GamePhase.SETTLEMENT_1.value:
            if not self.road and (
                self.vertex_set[0] == current_vertex
                or self.vertex_set[1] == current_vertex
            ):
                return True

        # # Only for non-settlement phase (need player logic too)
        # for edge in edges:
        #     if (
        #         edge.vertex_set[0] in self.vertex_set
        #         or edge.vertex_set[1] in self.vertex_set
        #     ) and edge.road:
        #         return True
        return False
