# Created by M. Krouwel
# based on work by BDMarius https://github.com/bdmarius/nn-connect4
from boardconverter import BoardConverter

if __name__ == "__main__":
    game : Game = Game()
    game.board = BoardConverter.convertFromString('0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-2-1-2-1-0')       
    print(game.isValid(2))