import copy
from typing import List, Tuple
from game import Game
from boardvalue import BoardValue
from player import Player

class GameController:

    game : Game
    redPlayer : Player
    bluePlayer : Player
    trainingHistory : List[Tuple[int, List[List[BoardValue]]]]

    def __init__(self, game : Game, redPlayer : Player, bluePlayer : Player):
        self.game = game
        self.redPlayer = redPlayer
        self.bluePlayer = bluePlayer
        self.trainingHistory = []

    def simulateManyGames(self, numberOfGames : int):
        redPlayerWins : int = 0
        bluePlayerWins : int = 0
        draws : int = 0
        for i in range(numberOfGames):
            self.game.resetBoard()
            self.playGame()
            if self.game.getGameResult() == BoardValue.RED_PLAYER_VAL:
                redPlayerWins = redPlayerWins + 1
            elif self.game.getGameResult() == BoardValue.BLUE_PLAYER_VAL:
                bluePlayerWins = bluePlayerWins + 1
            else:
                draws = draws + 1
            if i % 100 == 0:
                print(i)
        totalWins = redPlayerWins + bluePlayerWins + draws
        print('Red Wins: ' + str(int(redPlayerWins * 100 / totalWins)) + '%')
        print('Blue Wins: ' + str(int(bluePlayerWins * 100 / totalWins)) + '%')
        print('Draws: ' + str(int(draws * 100 / totalWins)) + '%')

    def playGame(self):
        #print('playong')
        playerToMove = self.redPlayer
        while self.game.getGameResult() == Game.GAME_STATE_NOT_ENDED:
            availableMoves = self.game.getAvailableMoves()
            move : List[int] = playerToMove.getMove(availableMoves, self.game.board)
            self.game.move(move, playerToMove)
            if playerToMove == self.redPlayer:
                playerToMove = self.bluePlayer
            else:
                playerToMove = self.redPlayer

        for historyItem in self.game.boardHistory:
            self.trainingHistory.append((self.game.getGameResult(), copy.deepcopy(historyItem)))