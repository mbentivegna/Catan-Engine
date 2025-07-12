import random
from typing import List
import pygame
from board import Board
from constants import Color, GamePhase
from player import Player
from vertex import Vertex


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1100, 800))
        self.board = Board(self.screen)
        randomized_list = self.randomize_player_cpu_order()
        self.players = [
            Player(1, "Player 1", randomized_list[0]),
            Player(2, "Player 2", randomized_list[1]),
            Player(3, "Player 3", randomized_list[2]),
            Player(4, "Player 4", randomized_list[3]),
        ]
        self.game_phase = GamePhase.SETTLEMENT_0.value

        self.start_game()

    @staticmethod
    def randomize_player_cpu_order() -> List[bool]:
        # Get order of player and cpu
        player_order = [False, False, False, True]
        random.shuffle(player_order)

        return player_order

    def start_game(self):
        clock = pygame.time.Clock()
        running = True

        # TODO:
        # Make UI better for which player is up and which vertices can be settled on
        # Make each player have a list of already settlements
        # Player / CPU roles and actions (create better heuristic)

        # Current Player
        current_player_index = 0
        number_of_turns = 0
        current_vertex = None

        WAIT_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(WAIT_EVENT, 2000)

        self.show_whose_turn(self.players[current_player_index])
        # Run game
        while running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self.game_phase in [
                    GamePhase.SETTLEMENT_0.value,
                    GamePhase.SETTLEMENT_1.value,
                ]:
                    if self.players[current_player_index].is_human:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            vertex = self.board.check_if_vertex_collision(mouse_pos)
                            if (
                                vertex
                                and self.game_phase == GamePhase.SETTLEMENT_0.value
                            ):
                                current_vertex = vertex
                                self.board.create_settlement(
                                    vertex, self.players[current_player_index]
                                )
                                self.game_phase = GamePhase.SETTLEMENT_1.value
                            edge = self.board.check_if_edge_collision(
                                mouse_pos,
                                self.players[current_player_index],
                                self.game_phase,
                                current_vertex,
                            )
                            if edge and self.game_phase == GamePhase.SETTLEMENT_1.value:
                                self.board.create_road(
                                    edge, self.players[current_player_index]
                                )
                                self.game_phase = GamePhase.SETTLEMENT_0.value
                                number_of_turns += 1
                                if number_of_turns > 7:
                                    self.game_phase = GamePhase.NON_SETTLEMENT.value
                                elif number_of_turns > 3:
                                    current_player_index = 7 - number_of_turns
                                else:
                                    current_player_index = number_of_turns
                                self.show_whose_turn(self.players[current_player_index])
                    else:
                        if event.type == WAIT_EVENT:
                            self.computer_settlement_phase(
                                self.players[current_player_index]
                            )
                            number_of_turns += 1
                            if number_of_turns > 7:
                                self.game_phase = GamePhase.NON_SETTLEMENT.value
                            elif number_of_turns > 3:
                                current_player_index = 7 - number_of_turns
                            else:
                                current_player_index = number_of_turns
                            self.show_whose_turn(self.players[current_player_index])

    def computer_heuristic(self, possible_vertices: List[Vertex]) -> Vertex:
        best_vertex_score = 0
        best_vertex = None
        for vertex in possible_vertices:
            current_score = 0
            for tile in vertex.tile_association:
                current_score += tile.tile_num_to_prob()

            if current_score > best_vertex_score:
                best_vertex_score = current_score
                best_vertex = vertex

        return best_vertex

    def computer_settlement_phase(self, player: Player) -> None:
        # Computer settle
        possible_vertices = self.board.get_list_of_settleable_vertices()
        vertex_to_settle = self.computer_heuristic(possible_vertices)
        self.board.create_settlement(vertex_to_settle, player)

        # Computer build road
        possible_edges = self.board.get_list_of_edges_off_vertex(vertex_to_settle)
        edge_to_settle = random.choice(possible_edges)
        self.board.create_road(edge_to_settle, player)

    def show_whose_turn(self, player: Player):
        # Show who is currently settling in the bottom left
        font = pygame.font.Font(None, 36)
        computer_str = "(Computer)"
        # there is definitely a better way to do this (write over the previous name)
        if player.is_human:
            computer_str = "                       "

        text = "It is " + player.name + "'s turn! " + computer_str

        text_surface = font.render(text, True, player.color)  # White text
        text_rect = text_surface.get_rect()

        padding = 10
        text_rect.topleft = (
            padding,
            self.screen.get_height() - text_rect.height - padding,
        )
        # Write whose turn it is on the screen
        pygame.draw.rect(self.screen, Color.BACKGROUND.to_rgb(), text_rect)
        self.screen.blit(text_surface, text_rect)

        pygame.display.flip()

    pygame.quit()
