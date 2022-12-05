# Created by M. Krouwel
# Class for solving game through model (tensor flow) prediction

import copy
from game import Game, GameSettings
from utils import Utils
from typing import List, Any, Tuple
from enums import AILevel
from C4model import ConnectFourModel

class ModelSolver:
    @staticmethod
    def run(gameSettings : GameSettings, board : List[List[int]], currentPlayer : int, level : AILevel, model : ConnectFourModel) -> Tuple[int, int]:
        avMovesWithValue : List[Tuple[Tuple[int, int], Any]]= []
        availableMoves : List[Tuple[int, int]] = Game.sgetAvailableMoves(gameSettings, board)

        for availableMove in availableMoves:
            boardCopy : List[List[int]] = copy.deepcopy(board)
            boardCopy[availableMove[0]][availableMove[1]] = currentPlayer
            mvalue = model.predict(boardCopy, currentPlayer)
            avMovesWithValue.append((availableMove, mvalue))
            
        avMovesWithValue.sort(key=Utils.takeSecond, reverse=True)
        return avMovesWithValue[min(level.value, len(avMovesWithValue)-1)][0]