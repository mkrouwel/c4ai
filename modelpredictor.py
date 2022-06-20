# Created by M. Krouwel
import copy
from utils import Utils
from typing import List, Any, Tuple
from ailevel import AILevel
from model import ConnectFourModel

class ModelPredictor:
    @staticmethod
    def run(availableMoves : List[Tuple[int, int]], board : List[List[int]], currentPlayer : int, level : AILevel, model : ConnectFourModel) -> Tuple[int, int]:
        avMovesWithValue : List[Tuple[Tuple[int, int], Any]]= []
        
        for availableMove in availableMoves:
            boardCopy : List[List[int]] = copy.deepcopy(board)
            boardCopy[availableMove[0]][availableMove[1]] = currentPlayer
            mvalue = model.predict(boardCopy, currentPlayer)
            avMovesWithValue.append((availableMove, mvalue))
            
        avMovesWithValue.sort(key=Utils.takeSecond, reverse=True)
        return avMovesWithValue[min(level.value, len(avMovesWithValue)-1)][0]