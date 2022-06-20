# Created by M. Krouwel
# based on work by Marius Borcan https://github.com/bdmarius/nn-connect4
import copy
import random
from typing import List, Tuple
from game import Game
from player import Player

class GameController:

    game : Game
    redPlayer : Player
    bluePlayer : Player
    trainingHistory : List[Tuple[int, List[List[int]]]]

    def __init__(self, game : Game, redPlayer : Player, bluePlayer : Player):
        self.game = game
        self.redPlayer = redPlayer
        self.bluePlayer = bluePlayer
        self.trainingHistory = []

    def simulateManyGames(self, numberOfGames : int, reportEvery : int):
        redPlayerWins : int = 0
        bluePlayerWins : int = 0
        draws : int = 0
        for i in range(numberOfGames):
            self.game.resetBoard()
            self.playGame()
            if self.game.getGameResult() == Game.RED_PLAYER_VAL:
                redPlayerWins = redPlayerWins + 1
            elif self.game.getGameResult() == Game.BLUE_PLAYER_VAL:
                bluePlayerWins = bluePlayerWins + 1
            else:
                draws = draws + 1
            if i % reportEvery == 0:
                print(i)
        totalWins = redPlayerWins + bluePlayerWins + draws
        print('Red Wins: ' + str(int(redPlayerWins * 100 / totalWins)) + '%')
        print('Blue Wins: ' + str(int(bluePlayerWins * 100 / totalWins)) + '%')
        print('Draws: ' + str(int(draws * 100 / totalWins)) + '%')

    def playGame(self):
        playerToMove = self.redPlayer if random.randrange(0,2) == 0 else self.bluePlayer
        while self.game.getGameResult() == Game.GAME_STATE_NOT_ENDED:
            move : Tuple[int, int] = playerToMove.getMove(self.game.getAvailableMoves(), self.game.board)
            self.game.move(move, playerToMove)
            if playerToMove == self.redPlayer:
                playerToMove = self.bluePlayer
            else:
                playerToMove = self.redPlayer

        for historyItem in self.game.boardHistory:
            self.trainingHistory.append((self.game.getGameResult(), copy.deepcopy(historyItem)))