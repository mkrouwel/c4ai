# Created by M. Krouwel
# inspired by Marius Borcan https://github.com/bdmarius/nn-connect4 and Keith Galli https://github.com/KeithGalli/Connect4-Python/blob/master/connect4.py
import copy
from typing import List, Tuple
from enum import Enum

import numpy as np
from utils import Utils

class GameState(Enum):
    DRAW : int = 0
    NOT_ENDED : int = -1
    ENDED : int = 1

class Game:
    NUM_ROWS : int = 6
    NUM_COLUMNS : int = 7

    EMPTY_VAL : int = 0
    BLUE_PLAYER_VAL : int = 1
    RED_PLAYER_VAL : int = -BLUE_PLAYER_VAL

    PLAYER_VALS : Tuple[int, int] = (BLUE_PLAYER_VAL, RED_PLAYER_VAL)
    BOARD_VALS : List[int] = [EMPTY_VAL, BLUE_PLAYER_VAL, RED_PLAYER_VAL]

    NR_TO_CONNECT : int = 4
    APPLY_GRAVITY : bool = True

    __board : List[List[int]]
    __boardHistory : List[List[List[int]]]

    def __init__(self):
        self.resetBoard()
    
    def resetBoard(self):
        self.__board = np.full((Game.NUM_ROWS, Game.NUM_COLUMNS), Game.EMPTY_VAL)
        self.__boardHistory = []

    def getBoard(self) -> List[List[int]]:
        return self.__board

    def setBoard(self, board : List[List[int]]):
        self.__board = board

    def getBoardHistory(self) -> List[List[List[int]]]:
        return self.__boardHistory

    @staticmethod
    def getOtherPlayer(currentPlayer : int) -> int:
        if currentPlayer in Game.PLAYER_VALS:
            return Game.RED_PLAYER_VAL if currentPlayer == Game.BLUE_PLAYER_VAL else Game.BLUE_PLAYER_VAL
        return 0

    @staticmethod
    def isValid(board: List[List[int]], currentPlayer : int) -> bool:
        # check for invalid values
        flattenedList : List[int] = Utils.flatten(board)
        if len(list(filter(lambda v : v not in Game.BOARD_VALS, flattenedList))) > 0:
            print('invalid value')
            return False

        # check player value
        if currentPlayer not in Game.PLAYER_VALS:
            print('not a valid player value')
            return False

        if Game.APPLY_GRAVITY:
            # check for non zero above zero
            nonZeroFound : bool
            for c in range(Game.NUM_COLUMNS):
                nonZeroFound = False
                for r in range(Game.NUM_ROWS):
                    if board[r][c] in Game.PLAYER_VALS:
                        nonZeroFound = True
                    elif nonZeroFound and board[r][c] == Game.EMPTY_VAL:
                        print('zero after nonzer')
                        return False 
        
        # check current player
        nrOfBlueStones : int = len(Utils.filterEqual(flattenedList, Game.BLUE_PLAYER_VAL))
        nrOfRedStones : int = len(Utils.filterEqual(flattenedList, Game.RED_PLAYER_VAL))

        if nrOfBlueStones == nrOfRedStones:
            #print('stones equal')
            return True

        if currentPlayer == Game.RED_PLAYER_VAL:
            #print(nrOfBlueStones == nrOfRedStones + 1)
            return nrOfBlueStones == nrOfRedStones + 1

        if currentPlayer == Game.BLUE_PLAYER_VAL:
            #print(nrOfBlueStones + 1 == nrOfRedStones)
            return nrOfBlueStones + 1 == nrOfRedStones

        print('somehow ended up here...', currentPlayer)
        return False

    def getAvailableMoves(self) -> List[Tuple[int, int]]:
        return Game.sgetAvailableMoves(self.__board)

    @staticmethod
    def sgetAvailableMoves(board : List[List[int]]) -> List[Tuple[int, int]]:
        availableMoves : List[Tuple[int, int]] = []
        if Game.APPLY_GRAVITY:
            for c in range(Game.NUM_COLUMNS):
                if board[Game.NUM_ROWS - 1][c] == Game.EMPTY_VAL:
                    availableMoves.append((Game.NUM_ROWS - 1, c))
                else:
                    for r in range(Game.NUM_ROWS - 1):
                        if board[r][c] == Game.EMPTY_VAL and board[r + 1][c] != Game.EMPTY_VAL:
                            availableMoves.append((r, c))  
        else:
            for r in range(Game.NUM_ROWS):
                for c in range(Game.NUM_COLUMNS):
                    if board[r][c] == Game.EMPTY_VAL:
                        availableMoves.append((r, c))
        return availableMoves

    def getGameResult(self) -> Tuple[GameState, int]:
        return Game.sgetGameResult(self.__board)

    @staticmethod
    def sgetGameResult(board : List[List[int]]) -> Tuple[GameState, int]:
        # Find winner on horizontal
        for r in range(Game.NUM_ROWS):
            for c in range(Game.NUM_COLUMNS - Game.NR_TO_CONNECT + 1):
                #print('h', r, c, board[r][c], [board[r][c+i] for i in range(1,Game.NR_TO_CONNECT)])
                if board[r][c] != Game.EMPTY_VAL and all([board[r][c+i] == board[r][c] for i in range(1,Game.NR_TO_CONNECT)]):
                    #print('horizontal found', board)
                    return (GameState.ENDED, board[r][c])

        # Find winner on vertical
        for c in range(Game.NUM_COLUMNS):
            for r in range(Game.NUM_ROWS - Game.NR_TO_CONNECT + 1):
                #print('v', r, c, board[r][c], [board[r+i][c] for i in range(1,Game.NR_TO_CONNECT)])
                if board[r][c] != Game.EMPTY_VAL and all([board[r+i][c] == board[r][c] for i in range(1,Game.NR_TO_CONNECT)]):
                    #print('vertical found', board)
                    return (GameState.ENDED, board[r][c])

        # Check left diagonals
        for r in range(Game.NUM_ROWS - Game.NR_TO_CONNECT + 1):
            for c in range(Game.NUM_COLUMNS - Game.NR_TO_CONNECT + 1):
                #print('l', r, c, board[r][c], [board[r+i][c+i] for i in range(1,Game.NR_TO_CONNECT)])
                if board[r][c] != Game.EMPTY_VAL and all([board[r+i][c+i] == board[r][c] for i in range(1,Game.NR_TO_CONNECT)]):
                    #print('left diagonal', board)
                    return (GameState.ENDED, board[r][c])

        # Check right diagonals
        for r in range(Game.NUM_ROWS - Game.NR_TO_CONNECT + 1):
            for c in range(Game.NUM_COLUMNS - Game.NR_TO_CONNECT + 1):
                #print('r', r, c, board[r+3][c], [board[r+3-i][c+i] for i in range(1,Game.NR_TO_CONNECT)])
                if board[r+Game.NR_TO_CONNECT-1][c] != Game.EMPTY_VAL and all([board[r+Game.NR_TO_CONNECT-1-i][c+i] == board[r+Game.NR_TO_CONNECT-1][c] for i in range(1,Game.NR_TO_CONNECT)]):
                    #print('right diagonal', board)
                    return (GameState.ENDED, board[r+Game.NR_TO_CONNECT-1][c])

        # check for draw (no empty fields)
        if len(list(filter(lambda v : v == Game.EMPTY_VAL, Utils.flatten(board)))) == 0:
            return (GameState.DRAW, 0)

        return (GameState.NOT_ENDED, 0)

    def move(self, move : Tuple[int, int], currentPlayerValue : int):
        self.__board[move[0]][move[1]] = currentPlayerValue
        self.__boardHistory.append(copy.deepcopy(self.__board))