# Created by M. Krouwel
from pathlib import Path
from typing import List, Optional
from boardconverter import BoardConverter
from game import Game, GameSettings
from gamecontroller import GameController
from model import ConnectFourModel
from player import Player
from enums import PlayerStrategy

if __name__ == "__main__":
    
    #print(board)
    #print(Game.isValid(board, Game.RED_PLAYER_VAL))

    gs : GameSettings = GameSettings(numRows=7)
    board : List[List[int]] = BoardConverter.convertFromString('0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-1', gs.numRows, gs.numCols, lambda v : -1 if v == 2 else v)

    model : Optional[ConnectFourModel] = None
    modelPath : str
    path : Path
    modelPath = f'./model_{gs.numRows}x{gs.numCols}_{gs.nrToConnect}_{gs.applyGravity}'
    print('loading: ', modelPath)
    path = Path(modelPath)
    if path.exists() and path.is_dir():
        model = ConnectFourModel(gs.numRows * gs.numCols, 3, 50)
        model.load(modelPath)

    model.predict(board, 0)
    #gc = GameController(Game(gs), Player(Game.BLUE_PLAYER_VAL, PlayerStrategy.MANUAL), Player(Game.RED_PLAYER_VAL, PlayerStrategy.MODEL, model=model))
    #print(gc.playGame())