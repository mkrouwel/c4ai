# Created by M. Krouwel
# based on work by Marius Borcan https://github.com/bdmarius/nn-connect4
# Class for controlling a game with 2 players
# Provides functions to play a single game (until it has been ended) and to simulate multiple games

import copy
import random
from typing import List, Tuple
from game import Game
from enums import GameState
from player import Player
from utils import Utils

class GameController:

    __game : Game
    __redPlayer : Player
    __bluePlayer : Player
    __trainingHistory : List[Tuple[int, List[List[int]]]]

    def __init__(self, game : Game, redPlayer : Player, bluePlayer : Player):
        self.__game = game
        self.__trainingHistory = []
        self.setPlayers(redPlayer, bluePlayer)

    def getTrainingHistory(self) -> List[Tuple[int, List[List[int]]]]:
        return self.__trainingHistory

    def setPlayers(self, redPlayer : Player, bluePlayer : Player):
        if redPlayer.getValue() == bluePlayer.getValue():
            raise ValueError('players should not have same value')
        self.__redPlayer = redPlayer
        self.__bluePlayer = bluePlayer

    # simulate multiple games and prints results  
    def simulateManyGames(self, numberOfGames : int, reportEvery : int):
        redPlayerWins : int = 0
        bluePlayerWins : int = 0
        draws : int = 0

        for i in range(numberOfGames):
            result : GameState
            winner : int
            result, winner = self.playGame()
            
            if result == GameState.DRAW:
                draws = draws + 1
            elif winner == Game.RED_PLAYER_VAL:
                redPlayerWins = redPlayerWins + 1
            elif winner == Game.BLUE_PLAYER_VAL:
                bluePlayerWins = bluePlayerWins + 1
                
            if i % reportEvery == 0:
                print(i)

        totalWins = redPlayerWins + bluePlayerWins + draws
        print('Red Wins: ' + str(int(redPlayerWins * 100 / totalWins)) + '%')
        print('Blue Wins: ' + str(int(bluePlayerWins * 100 / totalWins)) + '%')
        print('Draws: ' + str(int(draws * 100 / totalWins)) + '%')

    # plays a single game until it has finished (draw or winner)
    def playGame(self) -> Tuple[GameState, int]:
        # reset board
        self.__game.resetBoard()
        # randomly choose player to start
        playerToMove = self.__redPlayer if random.randint(0, 1) == 0 else self.__bluePlayer

        result : GameState = GameState.NOT_ENDED
        winner : int
        while result == GameState.NOT_ENDED:
            move : Tuple[int, int] = playerToMove.getMove(self.__game.getGameSettings(), self.__game.getBoard())
            self.__game.move(move, playerToMove.getValue())
            if playerToMove == self.__redPlayer:
                playerToMove = self.__bluePlayer
            else:
                playerToMove = self.__redPlayer
            result, winner = self.__game.getGameResult()

        historyItem : List[List[int]]
        for historyItem in self.__game.getBoardHistory():
            self.__trainingHistory.append((Utils.takeSecond(self.__game.getGameResult()), copy.deepcopy(historyItem)))

        return result, winner