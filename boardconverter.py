from game import Game
from typing import List

from utils import Utils

class BoardConverter:

    SPLITTER : str = '-'

    @staticmethod
    def convertFromString(boardAsString : str) -> List[List[int]]:
        boardA = boardAsString.split(BoardConverter.SPLITTER)
        i = 0
        board : List[List[int]] = []
        for r in range(Game.NUM_ROWS) :
            row = []
            for c in range(Game.NUM_COLUMNS) :
                row.append(int(boardA[i]))
                i = i + 1
            board.append(row)
        return board

    @staticmethod
    def convertToString(board : List[List[int]]) -> str:
        return BoardConverter.SPLITTER.join(Utils.flatten(Game.board))