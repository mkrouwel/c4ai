# Created by M. Krouwel
# inspired by Keith Galli https://github.com/KeithGalli/Connect4-Python/blob/master/connect4.py
import copy
from math import inf
from typing import List, Tuple
from ailevel import AILevel
from utils import Utils
from game import Game, GameState
import random

class ABSolver:
    @staticmethod
    def run(board : List[List[int]], currentPlayer : int, level : AILevel) -> Tuple[int, int]:
        return Utils.takeFirst(ABSolver.minimax(board, currentPlayer, 3 - level.value, True, True, -inf, inf))
   
    @staticmethod
    def minimax(board : List[List[int]], currentPlayer : int, depth : int, maximizing : bool, useAB : bool, alpha : float, beta : float) -> Tuple[Tuple[int, int],float]:
        result : GameState
        winner : int

        result, winner = Game.sgetGameResult(board)
        if result == GameState.ENDED:
            if winner == currentPlayer:
                return ((-1,-1), 1000)
            else:
                return ((-1,-1), -1000)
        if result == GameState.DRAW:
            return ((-1,-1), 0)
        
        if depth == 0:
            return ((-1,-1), ABSolver.score_position(board, currentPlayer))
        
        availableMoves : List[Tuple[int, int]] = Game.sgetAvailableMoves(board)
        avMovesWithValue : List[Tuple[Tuple[int, int], float]] = []
        
        for availableMove in availableMoves:
            boardCopy : List[List[int]] = copy.deepcopy(board)
            boardCopy[availableMove[0]][availableMove[1]] = currentPlayer if maximizing else Game.getOtherPlayer(currentPlayer)
            score : float = Utils.takeSecond(ABSolver.minimax(boardCopy, currentPlayer, depth - 1, not maximizing, useAB, alpha, beta))
            avMovesWithValue.append((availableMove, score))
            if useAB:
                if maximizing:
                    alpha = max(alpha, score)            
                else:
                    beta = min(beta, score)
                if alpha >= beta:
                    break     
             
        avMovesWithValue.sort(key=Utils.takeSecond, reverse=maximizing)
        #print(avMovesWithValue)
        avMovesWithBestValue = [av for av in avMovesWithValue if Utils.takeSecond(av) == Utils.takeSecond(avMovesWithValue[0])]
        if len(avMovesWithBestValue) > 1: # multiple best moves, randomize!
            return avMovesWithBestValue[random.randrange(0, len(avMovesWithBestValue))]
        return avMovesWithValue[0]

    @staticmethod
    def score_position(board : List[List[int]], currentPlayer : int) -> int:
        score : int = 0
        
        # score horizontal
        for r in range(Game.NUM_ROWS):
            for c in range(Game.NUM_COLUMNS - Game.NR_TO_CONNECT + 1):
                score += ABSolver.scoreSequence([board[r][c+i] for i in range(Game.NR_TO_CONNECT)], currentPlayer)
        
        # score vertical
        for c in range(Game.NUM_COLUMNS):
            for r in range(Game.NUM_ROWS - Game.NR_TO_CONNECT + 1):
                score += ABSolver.scoreSequence([board[r+i][c] for i in range(Game.NR_TO_CONNECT)], currentPlayer)

        # right diagonal
        for r in range(Game.NUM_ROWS - Game.NR_TO_CONNECT + 1):
            for c in range(Game.NUM_COLUMNS - Game.NR_TO_CONNECT + 1):
                score += ABSolver.scoreSequence([board[r+i][c+i] for i in range(Game.NR_TO_CONNECT)], currentPlayer)

        # left diagonal
        for r in range(Game.NUM_ROWS - Game.NR_TO_CONNECT + 1):
            for c in range(Game.NUM_COLUMNS - Game.NR_TO_CONNECT + 1):
                score += ABSolver.scoreSequence([board[r+3-i][c+i] for i in range(Game.NR_TO_CONNECT)], currentPlayer)

        return score

    @staticmethod
    def scoreSequence(sequence : List[int], currentPlayer : int) -> int:
        lc : int = len(Utils.filterEqual(sequence, currentPlayer))
        le : int = len(Utils.filterEqual(sequence, Game.EMPTY_VAL))
        lo : int = len(Utils.filterEqual(sequence, Game.getOtherPlayer(currentPlayer)))
        if lc == Game.NR_TO_CONNECT - 1 and le == 1:
            return 10
        elif lc == Game.NR_TO_CONNECT - 2 and le == 2:
            return 1
        elif lo == Game.NR_TO_CONNECT - 1 and le == 1:
            return -100
        return 0