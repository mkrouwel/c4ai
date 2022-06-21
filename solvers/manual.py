# Created by M. Krouwel
from typing import List, Tuple
from game import Game
from utils import Utils


class ManualSolver:
    @staticmethod
    def run(board : List[List[int]]) -> Tuple[int, int]:        
        print(board)
        availableMoves : List[Tuple[int, int]] = Game.sgetAvailableMoves(board)
        movesForCol : List[Tuple[int, int]] = []
        while len(movesForCol) == 0:
            try:
                col = int(input('Give column: '))
            except ValueError:
                continue
            movesForCol = list(filter(lambda m : Utils.takeSecond(m) == col, availableMoves))
        return movesForCol[0]