# Created by M. Krouwel
# based on work by Marius Borcan https://github.com/bdmarius/nn-connect4
from game import Game, GameSettings
from player import  Player
from gamecontroller import GameController
from model import ConnectFourModel
from enums import PlayerStrategy

if __name__ == "__main__":
    redRandomPlayer : Player = Player(Game.RED_PLAYER_VAL)
    blueRandomPlayer : Player = Player(Game.BLUE_PLAYER_VAL)

    redABPlayer : Player = Player(Game.RED_PLAYER_VAL, PlayerStrategy.AB)
    blueABPlayer : Player = Player(Game.BLUE_PLAYER_VAL, PlayerStrategy.AB)

    for numRows in range(6,7):
        for numCols in range(7,8):
            for nrToConnect in range(4,5): #3, min(numRows, numCols) + 1):
                for applyGravity in [True]:
                    print(numRows, numCols, nrToConnect, applyGravity)
                    gameController : GameController = GameController(Game(GameSettings(numRows, numCols, nrToConnect, applyGravity)), redRandomPlayer, blueRandomPlayer)
                    print ("Playing with random vs random strategies")
                    gameController.simulateManyGames(1000, 100)

                    gameController.setPlayers(redRandomPlayer, blueABPlayer)
                    print ("Playing with random vs AB strategies")
                    gameController.simulateManyGames(100, 100)

                    gameController.setPlayers(redABPlayer, blueRandomPlayer)
                    print ("Playing with AB vs random strategies")
                    gameController.simulateManyGames(100, 100)

                    gameController.setPlayers(redABPlayer, blueABPlayer)
                    print ("Playing with AB vs AB strategies")
                    gameController.simulateManyGames(100, 100)

                    model : ConnectFourModel = ConnectFourModel(numRows * numCols, 3, 50, 100)
                    model.train(gameController.getTrainingHistory())
                    model.model.save(f'./model_{numRows}x{numCols}_{nrToConnect}_{applyGravity}')

#    redNeuralPlayer : Player = Player(Game.RED_PLAYER_VAL, PlayerStrategy.MODEL, model=model)
#    blueNeuralPlayer : Player = Player(Game.BLUE_PLAYER_VAL, PlayerStrategy.MODEL, model=model)

#    gameController.setPlayers(redRandomPlayer, blueNeuralPlayer)
#    print ("Playing with random vs NN")
#    gameController.simulateManyGames(100, 100)

#    gameController.setPlayers(redNeuralPlayer, blueABPlayer)
#    print ("Playing with NN vs AB")
#    gameController.simulateManyGames(100, 100)

#    gameController = GameController(Game(), redNeuralPlayer, blueRandomPlayer)
#    print("Playing with red player as Neural Network")
#    gameController.simulateManyGames(10, 100)