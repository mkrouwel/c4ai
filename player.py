import random
import copy
from typing import List
from ailevel import AILevel
from boardvalue import BoardValue
from playerstrategy import PlayerStrategy

class Player:

    __value : BoardValue
    __level : AILevel
    __strategy : PlayerStrategy

    def __init__(self, value : BoardValue, strategy : PlayerStrategy = PlayerStrategy.RANDOM, level : AILevel = AILevel.HARD, model=None):
        self.__value = value
        self.__strategy = strategy
        self.__model = model
        self.__level = level

    def getMove(self, availableMoves : List[List[int]], board : List[List[int]]):
        match(self.__strategy):
            case PlayerStrategy.RANDOM | PlayerStrategy.AB:
                return availableMoves[random.randrange(0, len(availableMoves))]
            case PlayerStrategy.MODEL:
                avMovesWithValue = []
                for availableMove in availableMoves:
                    boardCopy = copy.deepcopy(board)
                    boardCopy[availableMove[0]][availableMove[1]] = self.value
                    mvalue = self.model.predict(boardCopy, self.__value)
                    avMovesWithValue.append((availableMove, mvalue))
                
                avMovesWithValue.sort(key= lambda e : e[1], reverse=True)
                return avMovesWithValue[min(self.__level, len(availableMoves)-1)][0]

    def getValue(self) -> BoardValue:
        return self.__value