import copy
from typing import List
from boardvalue import BoardValue
from player import Player
from utils import Utils

class Game:

    GAME_STATE_DRAW = -1
    GAME_STATE_NOT_ENDED = -2
    REQUIRED_SEQUENCE = 4

    NUM_ROWS : int = 6
    NUM_COLUMNS : int = 7

    board : List[List[BoardValue]]
    boardHistory : List[List[List[BoardValue]]]

    def __init__(self):
        self.resetBoard()
    
    def resetBoard(self):
        self.board = [
            [BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL],
            [BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL],
            [BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL],
            [BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL],
            [BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL],
            [BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL, BoardValue.EMPTY_VAL]
        ] #[[copy.copy(BoardValue.EMPTY_VAL)] * NUM_COLUMNS] * NUM_ROWS
        self.boardHistory = []

    def isValid(self) -> bool:
        for c in range(Game.NUM_COLUMNS):
            nonZeroFound : bool = False
            for r in range(Game.NUM_ROWS):
                if self.board[r][c] == BoardValue.BLUE_PLAYER_VAL or self.board[r][c] == BoardValue.RED_PLAYER_VAL:
                    nonzeroFound = True
                    #continue
                if nonZeroFound and self.board[r][c] == BoardValue.EMPTY_VAL:
                    return False
        return True

    def getAvailableMoves(self) -> List[List[int]]:
        availableMoves : List[List[int]] = []
        for c in range(Game.NUM_COLUMNS):
            if self.board[Game.NUM_ROWS - 1][c] == BoardValue.EMPTY_VAL:
                availableMoves.append([Game.NUM_ROWS - 1, c])
            else:
                for r in range(Game.NUM_ROWS - 1):
                    if self.board[r][c] == BoardValue.EMPTY_VAL and self.board[r + 1][c] != BoardValue.EMPTY_VAL:
                        availableMoves.append([r, c])
        return availableMoves

    def getGameResult(self) -> BoardValue | int:
        winnerFound : bool = False
        currentWinner : BoardValue = BoardValue.EMPTY_VAL
        # Find winner on horizontal
        for r in range(Game.NUM_ROWS):
            if not winnerFound:
                for c in range(Game.NUM_COLUMNS - Game.REQUIRED_SEQUENCE - 1):
                    if self.board[r][c] != BoardValue.EMPTY_VAL and self.board[r][c] == self.board[r][c+1] and self.board[r][c] == self.board[r][c + 2] and \
                            self.board[r][c] == self.board[r][c + 3]:
                        currentWinner = self.board[r][c]
                        winnerFound = True

        # Find winner on vertical
        if not winnerFound:
            for c in range(Game.NUM_COLUMNS):
                if not winnerFound:
                    for r in range(Game.NUM_ROWS - Game.REQUIRED_SEQUENCE - 1):
                        if self.board[r][c] != BoardValue.EMPTY_VAL and self.board[r][c] == self.board[r+1][c] and self.board[r][c] == self.board[r+2][c] and \
                                self.board[r][c] == self.board[r+3][c]:
                            currentWinner = self.board[r][c]
                            winnerFound = True

        # Check lower left diagonals
        if not winnerFound:
            for i in range(Game.NUM_ROWS - Game.REQUIRED_SEQUENCE - 1):
               j = 0
               while j <= i:
                   if self.board[i][j] != BoardValue.EMPTY_VAL and self.board[i][i] == self.board[i + 1][j + 1] and self.board[i][i] == self.board[i + 2][j + 2] and \
                           self.board[i][i] == self.board[i + 3][j + 3]:
                       currentWinner = self.board[i][j]
                       winnerFound = True
                   j = j+1

        # Check upper right diagonals
        if not winnerFound:
            for j in range(Game.NUM_COLUMNS - Game.REQUIRED_SEQUENCE - 1):
                i = j
                while i<= Game.NUM_ROWS - Game.REQUIRED_SEQUENCE - 1:
                    if self.board[i][j] != BoardValue.EMPTY_VAL and self.board[i][i] == self.board[i + 1][j + 1] and self.board[i][i] == self.board[i + 2][j + 2] and \
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
            #        if self.board[r][c] == BoardValue.EMPTY_VAL:
            #            drawFound = False
            #if drawFound:
            if len(list(filter(lambda v : v == BoardValue.EMPTY_VAL, Utils.flatten(self.board)))) == 0:
                return Game.GAME_STATE_DRAW  

            return Game.GAME_STATE_NOT_ENDED

    def move(self, move : List[int], player : Player):
        self.board[move[0]][move[1]] = player.getValue()
        self.boardHistory.append(copy.deepcopy(self.board))