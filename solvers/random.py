# Created by M. Krouwel
import random
from typing import List, Tuple

from game import Game

class RandomSolver:
    @staticmethod
    def run(board : List[List[int]]) -> Tuple[int, int]:
        availableMoves = Game.sgetAvailableMoves(board)
        return availableMoves[random.randrange(0, len(availableMoves))]