from game import Game
from player import  Player
from gamecontroller import GameController
from model import ConnectFourModel

if __name__ == "__main__":
    redRandomPlayer = Player(Game.RED_PLAYER_VAL, strategy='random')
    blueRandomPlayer = Player(Game.BLUE_PLAYER_VAL, strategy='random')

    gameController = GameController(Game(), redRandomPlayer, blueRandomPlayer)
    print ("Playing with both players with random strategies")
    gameController.simulateManyGames(1000)

    model = ConnectFourModel(42, 3, 50, 10)
    model.train(gameController.getTrainingHistory())

    redNeuralPlayer = Player(Game.RED_PLAYER_VAL, strategy='model', model=model)
    blueNeuralPlayer = Player(Game.BLUE_PLAYER_VAL, strategy='model', model=model)

    gameController = GameController(Game(), redRandomPlayer, blueNeuralPlayer)
    print ("Playing with blue player level Hard as Neural Network")
    gameController.simulateManyGames(1)

    gameController = GameController(Game(), redRandomPlayer, Player(Game.BLUE_PLAYER_VAL, level = 2, strategy='model', model=model))
    print ("Playing with blue player level Medium as Neural Network")
    gameController.simulateManyGames(1)

    gameController = GameController(Game(), redNeuralPlayer, blueRandomPlayer)
    print("Playing with red player as Neural Network")
    gameController.simulateManyGames(1)