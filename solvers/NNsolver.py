# Created by M. Krouwel
# Class for solving game through NN model prediction

import copy
from typing import List, Tuple
from numpy import exp, array, random, dot
from pyparsing import Any
from NN import NN
from enums import AILevel

from game import Game, GameSettings
from utils import Utils

class NNSolver:
    @staticmethod
    def run(gameSettings : GameSettings, board : List[List[int]], currentPlayer : int, level : AILevel, model : NN) -> Tuple[int, int]:
        avMovesWithValue : List[Tuple[Tuple[int, int], Any]]= []
        availableMoves : List[Tuple[int, int]] = Game.sgetAvailableMoves(gameSettings, board)

        for availableMove in availableMoves:
            boardCopy : List[List[int]] = copy.deepcopy(board)
            boardCopy[availableMove[0]][availableMove[1]] = currentPlayer
            mvalue = model.predict(boardCopy, currentPlayer)
            avMovesWithValue.append((availableMove, mvalue))
  
        avMovesWithValue.sort(key=Utils.takeSecond, reverse=True)
        return avMovesWithValue[min(level.value, len(avMovesWithValue)-1)][0]