from boardconverter import BoardConverter
from game import Game
from player import  Player
from gamecontroller import GameController
from model import ConnectFourModel
from playerstrategy import PlayerStrategy

if __name__ == "__main__":
#    print(Game.isValid(BoardConverter.convertFromString('0-2-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-1-2-1-0')))
    redRandomPlayer : Player = Player(Game.RED_PLAYER_VAL)
    blueRandomPlayer : Player = Player(Game.BLUE_PLAYER_VAL)

    gameController : GameController = GameController(Game(), redRandomPlayer, blueRandomPlayer)
    print ("Playing with both players with random strategies")
    gameController.simulateManyGames(1000)

#    model : ConnectFourModel = ConnectFourModel(42, 3, 50, 10)
#    model.train(gameController.trainingHistory)
#    model.model.save('./c4model')

#    redNeuralPlayer : Player = Player(Game.RED_PLAYER_VAL, PlayerStrategy.MODEL, model=model)
#    blueNeuralPlayer : Player = Player(Game.BLUE_PLAYER_VAL, PlayerStrategy.MODEL, model=model)

#    gameController = GameController(Game(), redRandomPlayer, blueNeuralPlayer)
#    print ("Playing with blue player level Hard as Neural Network")
#    gameController.simulateManyGames(1)

    #gameController = GameController(Game(), redRandomPlayer, Player(Game.BLUE_PLAYER_VAL, PlayerStrategy.MODEL, model))
    #print ("Playing with blue player level Medium as Neural Network")
    #gameController.simulateManyGames(1)

#    gameController = GameController(Game(), redNeuralPlayer, blueRandomPlayer)
#    print("Playing with red player as Neural Network")
#    gameController.simulateManyGames(1)