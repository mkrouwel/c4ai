# Created by M. Krouwel
# based on work by Marius Borcan https://github.com/bdmarius/nn-connect4
from typing import List
from boardconverter import BoardConverter
from game import Game
from gamecontroller import GameController
from player import Player
import numpy as np

from playerstrategy import PlayerStrategy

if __name__ == "__main__":
    #board : List[List[int]] = BoardConverter.convertFromString('0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-2-1-2-1-0', Game.NUM_ROWS, Game.NUM_COLUMNS, lambda v : -1 if v == 2 else v)
    #print(board)
    #print(Game.isValid(board, Game.RED_PLAYER_VAL))

    gc = GameController(Game(), Player(Game.BLUE_PLAYER_VAL, PlayerStrategy.MANUAL), Player(Game.RED_PLAYER_VAL, PlayerStrategy.AB))
    print(gc.playGame())
    #playerToMove = Player() if random.randint(0, 1) == 0 else self.__bluePlayer