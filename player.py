# Created by M. Krouwel
# based on work by Marius Borcan https://github.com/bdmarius/nn-connect4
from ast import AugAssign
from typing import List, Optional, Tuple
from AB import AB
from ailevel import AILevel
from model import ConnectFourModel
import random
from typing import List, Tuple
from modelpredictor import ModelPredictor
from playerstrategy import PlayerStrategy
from utils import Utils

class Player:

    __value : int
    __level : AILevel
    __strategy : PlayerStrategy
    __model : Optional[ConnectFourModel]

    def __init__(self, value : int, strategy : PlayerStrategy = PlayerStrategy.RANDOM, level : AILevel = AILevel.HARD, model : Optional[ConnectFourModel] = None):
        self.__value = value
        self.__strategy = strategy
        self.__model = model
        self.__level = level

        if self.__model == None and self.__strategy == PlayerStrategy.MODEL:
            self.__strategy = PlayerStrategy.RANDOM
            print('changing strategy, no model given')

    def getMove(self, availableMoves : List[Tuple[int, int]], board : List[List[int]]) -> Tuple[int, int]:
        match(self.__strategy):
            case PlayerStrategy.RANDOM:
                return availableMoves[random.randrange(0, len(availableMoves))]
            case PlayerStrategy.MANUAL:
                print(board)
                movesForCol : List[Tuple[int, int]] = []
                while len(movesForCol) == 0:
                    col = int(input('Give column'))
                    movesForCol = list(filter(lambda m : Utils.takeSecond(m) == col, availableMoves))
                return movesForCol[0]
            case PlayerStrategy.AB:
                return AB.run(availableMoves, board, self.__value)
            case PlayerStrategy.MODEL:
                if self.__model is not None:
                    return ModelPredictor.run(availableMoves, board, self.__value, self.__level, self.__model)
                raise NotImplementedError("No model provided")
            case _:
                raise NotImplementedError("Not implemented")

    def getValue(self) -> int:
        return self.__value