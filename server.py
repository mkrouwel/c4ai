# Created by M. Krouwel
from http.server import BaseHTTPRequestHandler, HTTPServer
from boardconverter import BoardConverter
from game import Game, GameSettings
from player import Player
from model import ConnectFourModel
from tensorflow import keras # type: ignore
import urllib.parse as urlparse
from typing import Any, List, Tuple
from enums import AILevel, PlayerStrategy, GameState
from utils import Utils

model = ConnectFourModel(42, 3, 50, 10) #TODO: 42 = numRows * numCols. Maybe only load model on call?
model.model = keras.models.load_model('./c4model')

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # parse input
        parsed_url : str = urlparse.urlparse(self.path)
        if parsed_url.path == '/move' and parsed_url.query != '':
            self.processMove(urlparse.parse_qs(parsed_url.query))

    def processMove(self, params : Any):
        # parse params
        f = lambda v : -1 if v == 2 else v
        currentplayer : int = f(int(params['currentplayer'][0]))
        level : AILevel = AILevel(int(params['level'][0]))
        board : List[List[int]] = BoardConverter.convertFromString(params['board'][0], gameSettings.numRows, gameSettings.numCols, f)
        solver : PlayerStrategy = PlayerStrategy(params['solver'][0])
        print(board)
        nextMove : Tuple[int, int] = (-1,-1)
        gameSettings : GameSettings = GameSettings()

        # check valid
        if Game.isValid(gameSettings, board, currentplayer) and Game.sgetGameResult(gameSettings, board) != GameState.NOT_ENDED:
            p : Player = Player(currentplayer, solver, level, model)
            nextMove = p.getMove(gameSettings, board)
            print(nextMove)
        else:
            print('board not valid or game already ended')

        # send result
        responseText = str(Utils.takeSecond(nextMove)).encode("utf-8")
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.send_header("Content-Length", str(len(responseText)))
        self.end_headers()
        self.wfile.write(responseText)

with HTTPServer(('', 8000), handler) as server:
    print('awaiting get call')
    server.serve_forever()