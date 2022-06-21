# Created by M. Krouwel
from enum import Enum

class AILevel(Enum):
    HARD = 0
    MEDIUM = 1
    EASY = 2

class GameState(Enum):
    DRAW : int = 0
    NOT_ENDED : int = -1
    ENDED : int = 1

class PlayerStrategy(Enum):
    RANDOM = 'RANDOM'
    MODEL = 'MODEL'
    AB = 'AB'
    MANUAL = 'MANUAL'