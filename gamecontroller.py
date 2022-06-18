import copy
from game import Game

class GameController:

    def __init__(self, game, redPlayer, bluePlayer):
        self.game = game
        self.redPlayer = redPlayer
        self.bluePlayer = bluePlayer
        self.trainingHistory = []

    def simulateManyGames(self, numberOfGames):
        redPlayerWins = 0
        bluePlayerWins = 0
        draws = 0
        for i in range(numberOfGames):
            self.game.resetBoard()
            self.playGame()
            if self.game.getGameResult() == Game.RED_PLAYER_VAL:
                redPlayerWins = redPlayerWins + 1
            elif self.game.getGameResult() == Game.BLUE_PLAYER_VAL:
                bluePlayerWins = bluePlayerWins + 1
            else:
                draws = draws + 1
        totalWins = redPlayerWins + bluePlayerWins + draws
        print('Red Wins: ' + str(int(redPlayerWins * 100 / totalWins)) + '%')
        print('Blue Wins: ' + str(int(bluePlayerWins * 100 / totalWins)) + '%')
        print('Draws: ' + str(int(draws * 100 / totalWins)) + '%')

    def playGame(self):
        playerToMove = self.redPlayer
        while self.game.getGameResult() == Game.GAME_STATE_NOT_ENDED:
            availableMoves = self.game.getAvailableMoves()
            move = playerToMove.getMove(availableMoves, self.game.getBoard())
            self.game.move(move, playerToMove.getPlayer())
            if playerToMove == self.redPlayer:
                playerToMove = self.bluePlayer
            else:
                playerToMove = self.redPlayer

        for historyItem in self.game.getBoardHistory():
            self.trainingHistory.append((self.game.getGameResult(), copy.deepcopy(historyItem)))

    def getTrainingHistory(self):
        return self.trainingHistory