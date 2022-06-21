# Created by M. Krouwel
from typing import List, Tuple
from game import Game
from utils import Utils


class ManualSolver:
    @staticmethod
    def run(board : List[List[int]]) -> Tuple[int, int]:        
        print(board)
        availableMoves : List[Tuple[int, int]] = Game.sgetAvailableMoves(board)
        movesForInput : List[Tuple[int, int]] = []
        while len(movesForInput) == 0:
            try:
                col = int(input('Give column: '))
            except ValueError:
                continue
            movesForInput = list(filter(lambda m : Utils.takeSecond(m) == col, availableMoves))
            
            if len(movesForInput) > 1:
                row : int = -1
                while(row == -1):
                    try:
                        row = int(input('Give row: '))
                    except ValueError:
                        continue
                movesForInput = list(filter(lambda m : Utils.takeFirst(m) == row, movesForInput))
        return movesForInput[0]