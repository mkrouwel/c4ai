# Created by M. Krouwel
# based on work by Marius Borcan https://github.com/bdmarius/nn-connect4
from typing import List, Tuple
from game import Game
from player import  Player
from gamecontroller import GameController
from model import ConnectFourModel
from playerstrategy import PlayerStrategy

if __name__ == "__main__":
    redRandomPlayer : Player = Player(Game.RED_PLAYER_VAL)
    blueRandomPlayer : Player = Player(Game.BLUE_PLAYER_VAL)

    redABPlayer : Player = Player(Game.RED_PLAYER_VAL, PlayerStrategy.AB)
    blueABPlayer : Player = Player(Game.BLUE_PLAYER_VAL, PlayerStrategy.AB)

    #data : List[Tuple[int, List[List[int]]]] = []

    gameController : GameController = GameController(Game(), redRandomPlayer, blueRandomPlayer)
    print ("Playing with random vs random strategies")
    gameController.simulateManyGames(1000, 100)

    gameController.setPlayers(redRandomPlayer, blueABPlayer)
    print ("Playing with random vs AB strategies")
    gameController.simulateManyGames(1000, 100)

    gameController.setPlayers(redABPlayer, blueRandomPlayer)
    print ("Playing with with AB vs random strategies")
    gameController.simulateManyGames(1000, 100)

    model : ConnectFourModel = ConnectFourModel(42, 3, 50, 100)
    #t : List[Tuple[int, List[List[int]]]] = gameController1.getTrainingHistory()
    #t.extend(gameController2.getTrainingHistory())
    model.train(gameController.getTrainingHistory())
    model.model.save('./c4model')

    redNeuralPlayer : Player = Player(Game.RED_PLAYER_VAL, PlayerStrategy.MODEL, model=model)
    blueNeuralPlayer : Player = Player(Game.BLUE_PLAYER_VAL, PlayerStrategy.MODEL, model=model)

    gameController = GameController(Game(), redRandomPlayer, blueNeuralPlayer)
    print ("Playing with blue player level Hard as Neural Network")
    gameController.simulateManyGames(1000, 100)

    #gameController = GameController(Game(), redRandomPlayer, Player(Game.BLUE_PLAYER_VAL, PlayerStrategy.MODEL, model))
    #print ("Playing with blue player level Medium as Neural Network")
    #gameController.simulateManyGames(1)

#    gameController = GameController(Game(), redNeuralPlayer, blueRandomPlayer)
#    print("Playing with red player as Neural Network")
#    gameController.simulateManyGames(1)