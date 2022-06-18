from http.server import BaseHTTPRequestHandler, HTTPServer
from boardconverter import BoardConverter
from game import Game
from player import Player
from model import ConnectFourModel
from tensorflow import keras
import urllib.parse as urlparse
from typing import List
from ailevel import AILevel
from playerstrategy import PlayerStrategy

model = ConnectFourModel(42, 3, 50, 10)
model.model = keras.models.load_model('./c4model')

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url : str = urlparse.urlparse(self.path)
        params : List[List[str]] = urlparse.parse_qs(parsed_url.query)
        #print(params)
        currentplayer : int = int(params['currentplayer'][0])
        level : AILevel = AILevel(int(params['level'][0]))
        board : List[List[int]] = BoardConverter.convertFromString(params['board'][0])         
        #print(currentplayer, level, board)
        nextMove = -1
        if Game.isValid(board):
            #print('board not valid!') 
            game : Game = Game()
            game.board = board
            p : Player = Player(currentplayer, PlayerStrategy.MODEL, level, model)
            nextMove = p.getMove(game.getAvailableMoves(), board)[1]
        responseText = str(nextMove).encode("utf-8")
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.send_header("Content-Length", str(len(responseText)))
        self.end_headers()
        self.wfile.write(responseText)

with HTTPServer(('', 8000), handler) as server:
    print('awaiting get call')
    server.serve_forever()