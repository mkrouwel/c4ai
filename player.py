# Created by M. Krouwel
# based on work by Marius Borcan https://github.com/bdmarius/nn-connect4
from typing import List, Optional, Tuple
from NN import NN
from enums import AILevel, PlayerStrategy
from game import GameSettings
from model import ConnectFourModel
from solvers import AB, random, modelsolver, manual, NNsolver

class Player:

    __value : int
    __level : AILevel
    __strategy : PlayerStrategy
    __model : Optional[ConnectFourModel | NN]

    def __init__(self, value : int, strategy : PlayerStrategy = PlayerStrategy.RANDOM, level : AILevel = AILevel.HARD, model : Optional[ConnectFourModel | NN] = None):
        self.__value = value
        self.__strategy = strategy
        self.__model = model
        self.__level = level

        if self.__model == None and self.__strategy == PlayerStrategy.MODEL:
            self.__strategy = PlayerStrategy.RANDOM
            print('changing strategy, no model given')

    def getMove(self, gameSettings : GameSettings, board : List[List[int]]) -> Tuple[int, int]:
        match(self.__strategy):
            case PlayerStrategy.RANDOM:
                return random.RandomSolver.run(gameSettings, board)
            case PlayerStrategy.MANUAL:
                return manual.ManualSolver.run(gameSettings, board)
            case PlayerStrategy.MINIMAX:
                return AB.ABSolver.run(gameSettings, board, self.__value, self.__level, False)
            case PlayerStrategy.AB:
                return AB.ABSolver.run(gameSettings, board, self.__value, self.__level, True)
            case PlayerStrategy.NN:
                if self.__model is not None and type(self.__model) == NN:
                    return NNsolver.NNSolver.run(gameSettings, board, self.__value, self.__level, self.__model)
                raise ValueError("No model provided")
            case PlayerStrategy.MODEL:
                if self.__model is not None and type(self.__model) == ConnectFourModel:
                    return modelsolver.ModelSolver.run(gameSettings, board, self.__value, self.__level, self.__model)
                raise ValueError("No model provided")
            case _:
                raise NotImplementedError("Not implemented")

    def getValue(self) -> int:
        return self.__value