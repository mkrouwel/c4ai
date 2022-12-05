# Created by M. Krouwel
# Class for solving game through random moves

import random
from typing import List, Tuple

from game import Game, GameSettings

class RandomSolver:
    @staticmethod
    def run(gameSettings : GameSettings, board : List[List[int]]) -> Tuple[int, int]:
        availableMoves = Game.sgetAvailableMoves(gameSettings, board)
        return availableMoves[random.randrange(0, len(availableMoves))]