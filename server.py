from http.server import BaseHTTPRequestHandler, HTTPServer
from game import Game
from player import Player
from model import ConnectFourModel
from tensorflow import keras
import urllib.parse as urlparse
#from keras.models import Sequential

model = ConnectFourModel(42, 3, 50, 10)
model.model = keras.models.load_model('./c4model')

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse.urlparse(self.path)
        params = urlparse.parse_qs(parsed_url.query)
        #print(params)
        currentplayer = int(params['currentplayer'][0])
        level = int(params['level'][0])
        boardA = params['board'][0].split('-')
        i = 0
        board = []
        for r in range(Game.NUM_ROWS) :
            row = []
            for c in range(Game.NUM_COLUMNS) :
                row.append(int(boardA[i]))
                i = i + 1
            board.append(row)
            
        #print(board)
        game = Game()
        game.board = board#= #TODO load board from request
        p = Player(currentplayer, level, strategy = 'model', model = model)
        nextMove = p.getMove(game.getAvailableMoves(), board)
        print(nextMove)
        responseText = str(nextMove[1]).encode("utf-8")
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.send_header("Content-Length", str(len(responseText)))
        self.end_headers()
        self.wfile.write(responseText)

with HTTPServer(('', 8000), handler) as server:
    server.serve_forever()