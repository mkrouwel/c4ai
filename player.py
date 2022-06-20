# Created by M. Krouwel
# based on work by Marius Borcan https://github.com/bdmarius/nn-connect4
import random
import copy
from typing import List, Optional, Tuple, Any
from ailevel import AILevel
from model import ConnectFourModel
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
            case PlayerStrategy.AB:
                return (0,0)
            case PlayerStrategy.MODEL:
                avMovesWithValue : List[Tuple[Tuple[int, int], Any]]= []
                if self.__model is not None:
                    for availableMove in availableMoves:
                        boardCopy : List[List[int]] = copy.deepcopy(board)
                        boardCopy[availableMove[0]][availableMove[1]] = self.__value
                        mvalue = self.__model.predict(boardCopy, self.__value)
                        avMovesWithValue.append((availableMove, mvalue))
                    
                avMovesWithValue.sort(key=Utils.takeSecond, reverse=True)
                return avMovesWithValue[min(self.__level.value, len(avMovesWithValue)-1)][0]

    def getValue(self) -> int:
        return self.__value