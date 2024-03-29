# Created by M. Krouwel
# Class for creating a server that can process (GET) requests to return best move for given board
# e.g. localhost:8000/move?currentplayer=2&level=1&board=0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-1-2-1-0&solver=MODEL&rows=6&cols=7&gravity=True&connect=8

from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from NN import NN
from boardconverter import BoardConverter
from game import Game, GameSettings
from player import Player
from C4model import ConnectFourModel
import urllib.parse as urlparse
from typing import Any, List, Optional, Tuple
from enums import AILevel, PlayerStrategy, GameState
from utils import Utils

class handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        # parse input
        parsed_url : urlparse.ParseResult = urlparse.urlparse(self.path)
        if parsed_url.path == '/move' and parsed_url.query != '':
            self.processMove(urlparse.parse_qs(parsed_url.query))

    def processMove(self, params : Any) -> None:
        # parse params
        f = lambda v : -1 if v == 2 else v
        try:
            currentplayer : int = f(int(params['currentplayer'][0]))
        except (ValueError, KeyError):
            self.sendError('error: current player not a valid number')
            return
        try:
            level : AILevel = AILevel(int(params['level'][0]))
        except (ValueError, KeyError):
            self.sendError('error: level not a valid level')
            return
        try:
            solver : PlayerStrategy = PlayerStrategy(params['solver'][0])
        except (ValueError, KeyError):
            self.sendError('error: solver not a valid strategy')
            return
        try:
            numRows : int = int(params['rows'][0])
        except (ValueError, KeyError):
            self.sendError('error: rows not a valid number')
            return
        try:
            numCols : int = int(params['cols'][0])
        except (ValueError, KeyError):
            self.sendError('error: cols not a valid number')
            return
        try:
            nrToConnect : int = int(params['connect'][0])
        except (ValueError, KeyError):
            self.sendError('error: connect not a valid number')
            return
        try:
            applyGravity : bool = bool(params['gravity'][0])
        except (ValueError, KeyError):
            self.sendError('error: gravity not a valid boolean')
            return
        try:
            board : List[List[int]] = BoardConverter.convertFromString(params['board'][0], numRows, numCols, f)
        except (ValueError, KeyError, IndexError):
            self.sendError('error: board not valid')
            return
        
        # load model
        model : Optional[ConnectFourModel | NN] = None
        modelPath : str
        path : Path
        if solver == PlayerStrategy.MODEL:
            modelPath = f'./model_{numRows}x{numCols}_{nrToConnect}_{applyGravity}'
            path = Path(modelPath)
            if path.exists() and path.is_dir():
                model = ConnectFourModel(numRows * numCols, 3, 50)
                model.load(modelPath)
            else:
                self.sendError(f'error: {modelPath} not found as model')
                return
        elif solver == PlayerStrategy.NN:
            modelPath = f'./nn/nn_{numRows}x{numCols}_{nrToConnect}_{applyGravity}.csv'
            path = Path(modelPath)
            if path.exists() and path.is_file():
                model = NN(numRows * numCols, 3)
                model.load(modelPath)
            else:
                self.sendError(f'error: {modelPath} not found as model')
                return

        print(board)
        nextMove : Tuple[int, int] = (-1,-1)
        gameSettings : GameSettings = GameSettings(numRows, numCols, nrToConnect, applyGravity)

        # check valid
        if Game.isValid(gameSettings, board, currentplayer) and Game.sgetGameResult(gameSettings, board) != GameState.NOT_ENDED:
            player : Player = Player(currentplayer, solver, level, model)
            nextMove = player.getMove(gameSettings, board)
            print(nextMove)
        else:
            self.sendError('board not valid or game already ended')
            return

        # send result
        if applyGravity:
            self.sendResponse(200, str(Utils.takeSecond(nextMove)))
        else:
            self.sendResponse(200, str(Utils.takeFirst(nextMove)) + ',' + str(Utils.takeSecond(nextMove)))

    def sendResponse(self, code : int, message : str) -> None:
        messageEncoded : bytes = message.encode("utf-8")
        self.send_response(code)
        self.send_header('Content-type','text/plain')
        self.send_header("Content-Length", str(len(messageEncoded)))
        self.end_headers()
        self.wfile.write(messageEncoded)

    def sendError(self, message : str) -> None:
        self.sendResponse(400, message)

with HTTPServer(('', 8000), handler) as server:
    print('awaiting get call')
    server.serve_forever()