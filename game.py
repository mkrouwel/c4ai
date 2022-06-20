# Created by M. Krouwel
# based on work by Marius Borcan https://github.com/bdmarius/nn-connect4
import copy
from os import stat
from typing import List, Tuple

import numpy as np
from player import Player
from utils import Utils

class Game:

    GAME_STATE_DRAW = -1
    GAME_STATE_NOT_ENDED = -2
    REQUIRED_SEQUENCE = 4

    NUM_ROWS : int = 6
    NUM_COLUMNS : int = 7

    EMPTY_VAL = 0
    BLUE_PLAYER_VAL = 1
    RED_PLAYER_VAL = 2

    board : List[List[int]]
    boardHistory : List[List[List[int]]]

    def __init__(self):
        self.resetBoard()
    
    def resetBoard(self):
        self.board = np.full((Game.NUM_ROWS, Game.NUM_COLUMNS), Game.EMPTY_VAL)
        self.boardHistory = []

    def isValid(self, currentPlayer : int) -> bool:
        flattenedList : List[int] = Utils.flatten(self.board)
        if len(list(filter(lambda v : v != Game.EMPTY_VAL and v != Game.BLUE_PLAYER_VAL and v != Game.RED_PLAYER_VAL, flattenedList))) > 0:
            return False

        nonZeroFound : bool
        for c in range(Game.NUM_COLUMNS):
            nonZeroFound = False
            for r in range(Game.NUM_ROWS):
                if self.board[r][c] == Game.BLUE_PLAYER_VAL or self.board[r][c] == Game.RED_PLAYER_VAL:
                    nonZeroFound = True
                elif nonZeroFound and self.board[r][c] == Game.EMPTY_VAL:
                    return False
        
        nrOfBlueStones : int = len(list(filter(lambda v : v == Game.BLUE_PLAYER_VAL, flattenedList)))
        nrOfRedStones : int = len(list(filter(lambda v : v == Game.RED_PLAYER_VAL, flattenedList)))

        if nrOfBlueStones == nrOfRedStones:
            return True

        if currentPlayer == Game.RED_PLAYER_VAL:
            return nrOfBlueStones == nrOfRedStones + 1

        if currentPlayer == Game.BLUE_PLAYER_VAL:
            return nrOfBlueStones + 1 == nrOfRedStones

        return False

    def getAvailableMoves(self) -> List[Tuple[int, int]]:
        availableMoves : List[Tuple[int, int]] = []
        for c in range(Game.NUM_COLUMNS):
            if self.board[Game.NUM_ROWS - 1][c] == Game.EMPTY_VAL:
                availableMoves.append((Game.NUM_ROWS - 1, c))
            else:
                for r in range(Game.NUM_ROWS - 1):
                    if self.board[r][c] == Game.EMPTY_VAL and self.board[r + 1][c] != Game.EMPTY_VAL:
                        availableMoves.append((r, c))
        return availableMoves

    def getGameResult(self) -> int:
        winnerFound : bool = False
        currentWinner : int = Game.EMPTY_VAL
        # Find winner on horizontal
        for r in range(Game.NUM_ROWS):
            if not winnerFound:
                for c in range(Game.NUM_COLUMNS - Game.REQUIRED_SEQUENCE - 1):
                    if self.board[r][c] != Game.EMPTY_VAL and self.board[r][c] == self.board[r][c+1] and self.board[r][c] == self.board[r][c + 2] and \
                            self.board[r][c] == self.board[r][c + 3]:
                        currentWinner = self.board[r][c]
                        winnerFound = True

        # Find winner on vertical
        if not winnerFound:
            for c in range(Game.NUM_COLUMNS):
                if not winnerFound:
                    for r in range(Game.NUM_ROWS - Game.REQUIRED_SEQUENCE - 1):
                        if self.board[r][c] != Game.EMPTY_VAL and self.board[r][c] == self.board[r+1][c] and self.board[r][c] == self.board[r+2][c] and \
                                self.board[r][c] == self.board[r+3][c]:
                            currentWinner = self.board[r][c]
                            winnerFound = True

        # Check lower left diagonals
        if not winnerFound:
            for i in range(Game.NUM_ROWS - Game.REQUIRED_SEQUENCE - 1):
               j = 0
               while j <= i:
                   if self.board[i][j] != Game.EMPTY_VAL and self.board[i][i] == self.board[i + 1][j + 1] and self.board[i][i] == self.board[i + 2][j + 2] and \
                           self.board[i][i] == self.board[i + 3][j + 3]:
                       currentWinner = self.board[i][j]
                       winnerFound = True
                   j = j+1

        # Check upper right diagonals
        if not winnerFound:
            for j in range(Game.NUM_COLUMNS - Game.REQUIRED_SEQUENCE - 1):
                i = j
                while i<= Game.NUM_ROWS - Game.REQUIRED_SEQUENCE - 1:
                    if self.board[i][j] != Game.EMPTY_VAL and self.board[i][i] == self.board[i + 1][j + 1] and self.board[i][i] == self.board[i + 2][j + 2] and \
                            self.board[i][i] == self.board[i + 3][j + 3]:
                        currentWinner = self.board[i][j]
                        winnerFound = True
                    i = i+1

        if winnerFound: return currentWinner
        else:
            # Check for draw 
            #drawFound : bool = True
            #for r in range(Game.NUM_ROWS):
            #    for c in range(Game.NUM_COLUMNS):
            #        if self.board[r][c] == Game.EMPTY_VAL:
            #            drawFound = False
            #if drawFound:
            if len(list(filter(lambda v : v == Game.EMPTY_VAL, Utils.flatten(self.board)))) == 0:
                return Game.GAME_STATE_DRAW  

            return Game.GAME_STATE_NOT_ENDED

    def move(self, move : Tuple[int, int], player : Player):
        self.board[move[0]][move[1]] = player.getValue()
        self.boardHistory.append(copy.deepcopy(self.board))