from enum import Enum
import math
from typing import Tuple


class Color(Enum):
    """
    Example to call color:
    Color.RED.to_rgb()
    """

    WOOD = "#68aa59"
    SHEEP = "#ea78f0"
    ORE = "#b7b7b7"
    DESERT = "#ffdfc0"
    WHEAT = "#d9ce0e"
    BRICK = "#e37d5e"

    BACKGROUND = "#81b1f0"
    VERTEX = "#5cd171"
    EDGE = "#dbb77d"
    OUTLINE = "#000000"
    HOUSE = "#02ccfe"

    PLAYER_1 = "#c0392b"
    PLAYER_2 = "#2980b9"
    PLAYER_3 = "#2ecc71"
    PLAYER_4 = "#a569bd"

    def to_rgb(self) -> Tuple[int, int, int]:
        hex_color = self.value.lstrip("#")
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    @staticmethod
    def resource_to_color(resource: str) -> Tuple[int, int, int]:
        match resource:
            case Resource.DESERT.value:
                return Color.DESERT.to_rgb()
            case Resource.SHEEP.value:
                return Color.SHEEP.to_rgb()
            case Resource.WHEAT.value:
                return Color.WHEAT.to_rgb()
            case Resource.ORE.value:
                return Color.ORE.to_rgb()
            case Resource.WOOD.value:
                return Color.WOOD.to_rgb()
            case Resource.BRICK.value:
                return Color.BRICK.to_rgb()
            case _:
                Color.OUTLINE.to_rgb()

    @staticmethod
    def player_id_to_color(id: int) -> Tuple[int, int, int]:
        match id:
            case 1:
                return Color.PLAYER_1.to_rgb()
            case 2:
                return Color.PLAYER_2.to_rgb()
            case 3:
                return Color.PLAYER_3.to_rgb()
            case 4:
                return Color.PLAYER_4.to_rgb()
            case _:
                Color.OUTLINE.to_rgb()


class Port(Enum):
    WHEAT_PORT = "Wheat Port"
    SHEEP_PORT = "Sheep Port"
    WOOD_PORT = "Wood Port"
    ORE_PORT = "Ore Port"
    BRICK_PORT = "Brick Port"
    THREE_FOR_ONE_PORT = "Three for One Port"
    NO_PORT = "No Port"

    @staticmethod
    def get_port(i: int) -> str:
        match i:
            case 2 | 3 | 5 | 7 | 22 | 28 | 51 | 54:
                return Port.THREE_FOR_ONE_PORT.value
            case 8 | 12:
                return Port.SHEEP_PORT.value
            case 16 | 21:
                return Port.BRICK_PORT.value
            case 38 | 43:
                return Port.WOOD_PORT.value
            case 39 | 44:
                return Port.ORE_PORT.value
            case 49 | 53:
                return Port.WHEAT_PORT.value
            case _:
                return Port.NO_PORT.value


class Resource(Enum):
    DESERT = "Desert"
    SHEEP = "Sheep"
    WHEAT = "Wheat"
    ORE = "Ore"
    WOOD = "Wood"
    BRICK = "Brick"


class GamePhase(Enum):
    SETTLEMENT_0 = 0
    SETTLEMENT_1 = 1
    NON_SETTLEMENT = 2


RESOURCE_DICT = {
    Resource.DESERT.value: 1,
    Resource.SHEEP.value: 4,
    Resource.WHEAT.value: 4,
    Resource.ORE.value: 3,
    Resource.WOOD.value: 4,
    Resource.BRICK.value: 3,
}

NUMBER_DICT = {
    2: 1,
    3: 2,
    4: 2,
    5: 2,
    6: 2,
    8: 2,
    9: 2,
    10: 2,
    11: 2,
    12: 1,
}

DICE_SUM_PROBABILITY = {
    -1: 0,
    2: 1 / 36,
    3: 2 / 36,
    4: 3 / 36,
    5: 4 / 36,
    6: 5 / 36,
    7: 6 / 36,
    8: 5 / 36,
    9: 4 / 36,
    10: 3 / 36,
    11: 2 / 36,
    12: 1 / 36,
}


# Hexagon parameters
HEX_SIZE = 60
HEX_RADIUS = HEX_SIZE * math.sqrt(3) / 2
HEX_WIDTH = HEX_SIZE * math.sqrt(3)
HEX_HEIGHT = HEX_SIZE * 1.5
OFFSET_Q = 2
OFFSET_R = 1
