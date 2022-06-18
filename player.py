import random
import copy
from game import Game

class Player:

    def __init__(self, value, level = 0, strategy='random', model=None):
        self.value = value
        self.strategy = strategy
        self.model = model
        self.level = level

    def getMove(self, availableMoves, board):
        if self.strategy == "random":
            return availableMoves[random.randrange(0, len(availableMoves))]
        else:
            avMovesWithValue = []
            for availableMove in availableMoves:
                boardCopy = copy.deepcopy(board)
                boardCopy[availableMove[0]][availableMove[1]] = self.value
                if self.value == Game.RED_PLAYER_VAL:
                    mvalue = self.model.predict(boardCopy, 2)
                else:
                   mvalue = self.model.predict(boardCopy, 1)
                avMovesWithValue.append((availableMove, mvalue))
            
            avMovesWithValue.sort(key= lambda e : e[1], reverse=True)
            return avMovesWithValue[min(self.level, len(availableMoves)-1)][0]

    def getPlayer(self):
        return self.value