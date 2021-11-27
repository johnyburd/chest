from dataclasses import dataclass
from chest.models import Piece, Color, Position
from chest.evaluate import alpha_beta, evaluate, find_best_move
from chest.utils import open_fen



if __name__ == '__main__':
    position = Position.from_fen("8/PK6/8/8/8/8/8/5k2")
    #position = Position.from_fen("7r/1k6/8/8/8/8/PPP5/K7")
    #position = Position.from_fen("K7/8/7R/8/3rrrr1/8/ppp5/k7")
    #position = Position.from_fen("kr6/8/RK6/8/8/8/8/8")

    start, end = find_best_move(position, Color.black, 6)
    file = chr(end % position.board_width + 65)
    rank = position.board_height - end // position.board_width
    print(f"{position.board[start]} -> {file}{rank} ({start}, {end})")
    fen = position.perform_move(start, end).to_fen()
    #print(fen)
    open_fen(fen)

    #print(evaluate(position))