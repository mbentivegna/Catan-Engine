from constants import Color


class Player:
    def __init__(self, id: int, name: str, is_human: bool):
        self.id = int
        self.name = name
        self.color = Color.player_id_to_color(id)
        self.is_human = is_human
