import random
import copy
from typing import List, Tuple, Any
from ailevel import AILevel
from model import ConnectFourModel
from playerstrategy import PlayerStrategy

class Player:

    __value : int
    __level : AILevel
    __strategy : PlayerStrategy
    __model : ConnectFourModel

    def __init__(self, value : int, strategy : PlayerStrategy = PlayerStrategy.RANDOM, level : AILevel = AILevel.HARD, model : ConnectFourModel =None):
        self.__value = value
        self.__strategy = strategy
        self.__model = model
        self.__level = level

    def getMove(self, availableMoves : List[List[int]], board : List[List[int]]):
        match(self.__strategy):
            case PlayerStrategy.RANDOM | PlayerStrategy.AB:
                return availableMoves[random.randrange(0, len(availableMoves))]
            case PlayerStrategy.MODEL:
                avMovesWithValue : List[Tuple[List[int], Any]]= []
                for availableMove in availableMoves:
                    boardCopy : List[List[int]] = copy.deepcopy(board)
                    boardCopy[availableMove[0]][availableMove[1]] = self.__value
                    mvalue = self.__model.predict(boardCopy, self.__value)
                    avMovesWithValue.append((availableMove, mvalue))
                
                avMovesWithValue.sort(key= lambda e : e[1], reverse=True)
                return avMovesWithValue[min(self.__level.value, len(availableMoves)-1)][0]

    def getValue(self) -> int:
        return self.__value