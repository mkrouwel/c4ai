# Created by M. Krouwel
# Class for converting board to string or v.v.

from typing import List
from utils import Utils

class BoardConverter:

    SPLITTER : str = '-'

    @staticmethod
    def convertFromString(boardAsString : str, numRows : int, numCols : int, replaceFunction = None) -> List[List[int]]:
        boardA = boardAsString.split(BoardConverter.SPLITTER)
        i = 0
        board : List[List[int]] = []
        for r in range(numRows) :
            row = []
            for c in range(numCols) :
                v : int = int(boardA[i])
                if replaceFunction is not None:
                    v = replaceFunction(v)
                row.append(v)
                i = i + 1
            board.append(row)
        return board

    @staticmethod
    def convertToString(board : List[List[int]]) -> str:
        return BoardConverter.SPLITTER.join(Utils.flatten(board))