# Created by M. Krouwel
# based on work by Marius Borcan https://github.com/bdmarius/nn-connect4
from typing import List, Optional, Tuple
from ailevel import AILevel
from model import ConnectFourModel
from playerstrategy import PlayerStrategy
from solvers import AB, random, modelsolver, manual

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

    def getMove(self, board : List[List[int]]) -> Tuple[int, int]:
        match(self.__strategy):
            case PlayerStrategy.RANDOM:
                return random.RandomSolver.run(board)
            case PlayerStrategy.MANUAL:
                return manual.ManualSolver.run(board)
            case PlayerStrategy.AB:
                return AB.ABSolver.run(board, self.__value, self.__level)
            case PlayerStrategy.MODEL:
                if self.__model is not None:
                    return modelsolver.ModelSolver.run(board, self.__value, self.__level, self.__model)
                raise NotImplementedError("No model provided")
            case _:
                raise NotImplementedError("Not implemented")

    def getValue(self) -> int:
        return self.__value