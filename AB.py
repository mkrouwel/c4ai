import copy
from math import inf
import numpy as np
from typing import List, Tuple
from ailevel import AILevel
from utils import Utils
from game import Game, GameState
import random

class AB:
    @staticmethod
    def run(availableMoves : List[Tuple[int, int]], board : List[List[int]], currentPlayer : int) -> Tuple[int, int]:
        avMovesWithValue : List[Tuple[Tuple[int, int], int]]= []

        for availableMove in availableMoves:
            boardCopy : List[List[int]] = copy.deepcopy(board)
            boardCopy[availableMove[0]][availableMove[1]] = currentPlayer
            result, winner = Game.sgetGameResult(boardCopy)

            score : int
            if result == GameState.DRAW:
                score = 0
            elif result == GameState.ENDED and winner == currentPlayer:
                score = 1000
            else:
                score = AB.score_position(boardCopy, currentPlayer)
            avMovesWithValue.append((availableMove, score))

        avMovesWithValue.sort(key=Utils.takeSecond, reverse=True)
        #print(avMovesWithValue)
        avMovesWithBestValue = [av for av in avMovesWithValue if Utils.takeSecond(av) == Utils.takeSecond(avMovesWithValue[0])]
        if len(avMovesWithBestValue) > 1: # multiple best moves, randomize!
            return Utils.takeFirst(avMovesWithBestValue[random.randrange(0, len(avMovesWithBestValue))])
        return Utils.takeFirst(avMovesWithValue[0])
   
    @staticmethod
    def minimax(board : List[List[int]], currentPlayer : int, depth : int, maximizing : bool) -> float:
        result : GameState
        winner : int

        result, winner = Game.sgetGameResult(board)
        if result == GameState.ENDED and winner == currentPlayer:
            return 1000
        if result == GameState.DRAW:
            return 0
        
        if depth == 0:
            return AB.score_position(board, currentPlayer)
        
        value : float
        boardCopy : List[List[int]]
        if maximizing:
            value = -inf
            for availableMove in Game.sgetAvailableMoves(board):
                boardCopy = copy.deepcopy(board)
                boardCopy[availableMove[0]][availableMove[1]] = currentPlayer
                value = max(value, AB.minimax(boardCopy, -currentPlayer, depth - 1, False))
            return value
        else:
            value = inf
            for availableMove in Game.sgetAvailableMoves(board):
                boardCopy = copy.deepcopy(board)
                boardCopy[availableMove[0]][availableMove[1]] = currentPlayer
                value = max(value, AB.minimax(boardCopy, -currentPlayer, depth - 1, True))
            return value

    @staticmethod
    def score_position(board : List[List[int]], currentPlayer : int) -> int:
        #print('scoring', board)
        score : int = 0
        
        # score horizontal
        for r in range(Game.NUM_ROWS):
            for c in range(Game.NUM_COLUMNS - Game.NR_TO_CONNECT + 1):
                score += AB.scoreSequence([board[r][c+i] for i in range(Game.NR_TO_CONNECT)], currentPlayer)
        
        # score vertical
        for c in range(Game.NUM_COLUMNS):
            for r in range(Game.NUM_ROWS - Game.NR_TO_CONNECT + 1):
                score += AB.scoreSequence([board[r+i][c] for i in range(Game.NR_TO_CONNECT)], currentPlayer)

        # right diagonal
        for r in range(Game.NUM_ROWS - Game.NR_TO_CONNECT + 1):
            for c in range(Game.NUM_COLUMNS - Game.NR_TO_CONNECT + 1):
                score += AB.scoreSequence([board[r+i][c+i] for i in range(Game.NR_TO_CONNECT)], currentPlayer)

        # left diagonal
        for r in range(Game.NUM_ROWS - Game.NR_TO_CONNECT + 1):
            for c in range(Game.NUM_COLUMNS - Game.NR_TO_CONNECT + 1):
                score += AB.scoreSequence([board[r+3-i][c+i] for i in range(Game.NR_TO_CONNECT)], currentPlayer)

        return score

    @staticmethod
    def scoreSequence(sequence : List[int], currentPlayer : int) -> int:
        lc : int = len(Utils.filterEqual(sequence, currentPlayer))
        le : int = len(Utils.filterEqual(sequence, Game.EMPTY_VAL))
        lo : int = len(Utils.filterEqual(sequence, -currentPlayer))
#        if lc == 4:
#            return 100
        if lc == Game.NR_TO_CONNECT - 1 and le == 1:
            return 10
        elif lc == Game.NR_TO_CONNECT - 2 and le == 2:
            return 1
        elif lo == Game.NR_TO_CONNECT - 1 and le == 1:
            return -100
        return 0