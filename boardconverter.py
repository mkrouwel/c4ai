from boardvalue import BoardValue
from game import Game
from typing import string, List

from utils import Utils

class BoardConverter:

    SPLITTER : string = '-'

    def convertFromString(boardAsString : string) -> List[List[BoardValue]]:
        boardA = boardAsString.split(BoardConverter.SPLITTER)
        i = 0
        board = []
        for r in range(Game.NUM_ROWS) :
            row = []
            for c in range(Game.NUM_COLUMNS) :
                row.append(int(boardA[i]))
                i = i + 1
            Game.append(row)

    def convertToString(board : List[List[BoardValue]]) -> string:
        return BoardConverter.SPLITTER.join(Utils.flatten(Game.board))