# Created by M. Krouwel
# inspired by Keith Galli https://github.com/KeithGalli/Connect4-Python/blob/master/connect4.py
import copy
from math import inf
from typing import List, Tuple
from enums import AILevel, GameState
from utils import Utils
from game import Game, GameSettings
import random

class ABSolver:
    @staticmethod
    def run(gameSettings : GameSettings, board : List[List[int]], currentPlayer : int, level : AILevel) -> Tuple[int, int]:
        return Utils.takeFirst(ABSolver.minimax(gameSettings, board, currentPlayer, 3 - level.value, True, True, -inf, inf))
   
    @staticmethod
    def minimax(gameSettings : GameSettings, board : List[List[int]], currentPlayer : int, depth : int, maximizing : bool, useAB : bool, alpha : float, beta : float) -> Tuple[Tuple[int, int],float]:
        result : GameState
        winner : int

        result, winner = Game.sgetGameResult(gameSettings, board)
        if result == GameState.ENDED:
            if winner == currentPlayer:
                return ((-1,-1), 1000)
            else:
                return ((-1,-1), -1000)
        if result == GameState.DRAW:
            return ((-1,-1), 0)
        
        if depth == 0:
            return ((-1,-1), ABSolver.score_position(gameSettings, board, currentPlayer))
        
        availableMoves : List[Tuple[int, int]] = Game.sgetAvailableMoves(gameSettings, board)
        avMovesWithValue : List[Tuple[Tuple[int, int], float]] = []
        
        for availableMove in availableMoves:
            boardCopy : List[List[int]] = copy.deepcopy(board)
            boardCopy[availableMove[0]][availableMove[1]] = currentPlayer if maximizing else Game.getOtherPlayer(currentPlayer)
            score : float = Utils.takeSecond(ABSolver.minimax(gameSettings, boardCopy, currentPlayer, depth - 1, not maximizing, useAB, alpha, beta))
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
    def score_position(gameSettings : GameSettings, board : List[List[int]], currentPlayer : int) -> int:
        score : int = 0
        
        # score horizontal
        for r in range(gameSettings.numRows):
            for c in range(gameSettings.numCols - gameSettings.nrToConnect + 1):
                score += ABSolver.scoreSequence(gameSettings, [board[r][c+i] for i in range(gameSettings.nrToConnect)], currentPlayer)
        
        # score vertical
        for c in range(gameSettings.numCols):
            for r in range(gameSettings.numRows - gameSettings.nrToConnect + 1):
                score += ABSolver.scoreSequence(gameSettings, [board[r+i][c] for i in range(gameSettings.nrToConnect)], currentPlayer)

        # right diagonal
        for r in range(gameSettings.numRows - gameSettings.nrToConnect + 1):
            for c in range(gameSettings.numCols - gameSettings.nrToConnect + 1):
                score += ABSolver.scoreSequence(gameSettings, [board[r+i][c+i] for i in range(gameSettings.nrToConnect)], currentPlayer)

        # left diagonal
        for r in range(gameSettings.numRows - gameSettings.nrToConnect + 1):
            for c in range(gameSettings.numCols - gameSettings.nrToConnect + 1):
                score += ABSolver.scoreSequence(gameSettings, [board[r+gameSettings.nrToConnect-1-i][c+i] for i in range(gameSettings.nrToConnect)], currentPlayer)

        return score

    @staticmethod
    def scoreSequence(gameSettings : GameSettings, sequence : List[int], currentPlayer : int) -> int:
        lc : int = len(Utils.filterEqual(sequence, currentPlayer))
        le : int = len(Utils.filterEqual(sequence, Game.EMPTY_VAL))
        lo : int = len(Utils.filterEqual(sequence, Game.getOtherPlayer(currentPlayer)))
        if lc == gameSettings.nrToConnect - 1 and le == 1:
            return 10
        elif lc == gameSettings.nrToConnect - 2 and le == 2:
            return 1
        elif lo == gameSettings.nrToConnect - 1 and le == 1:
            return -100
        return 0