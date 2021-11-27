from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Tuple
from string import digits



class Piece(str, Enum):
    king = 'k'
    queen = 'q'
    bishop = 'b'
    rook = 'r'
    pawn = 'p'
    knight = 'n'

piece_values = {
    Piece.queen: 9,
    Piece.rook: 5,
    Piece.bishop: 3,
    Piece.knight: 3,
    Piece.pawn: 1,
    Piece.king: 0,
}

class Color(str, Enum):
    black = 'black'
    white = 'white'

@dataclass
class Position:
    board_height: int
    board_width: int
    board: List[int]
    white_pieces: List[Tuple[Piece, int]]
    black_pieces: List[Tuple[Piece, int]]

    def __hash__(self):
        return hash(str(self.board))

    @classmethod
    def from_fen(self, fen: str):
        position = Position(8, 8, ['' for _ in range(8*8)], [], [])
        rows = fen.split('/')
        row_idx = 0
        for row in rows:
            column = 0
            for c in row:
                if c in digits:
                    column += int(c) - 1
                else:
                    position.board[position.board_width * row_idx + column] = c
                    if c.isupper():
                        position.white_pieces.append((c.lower(), position.board_width * row_idx + column))
                    else:
                        position.black_pieces.append((c, position.board_width * row_idx + column))
                column += 1
            row_idx += 1
        return position
        
    def to_fen(self):
        output = ''
        empties = 0
        for i, square in enumerate(self.board):
            if i % self.board_width == 0 and i > 0:
                if empties > 0:
                    output += str(empties)
                    empties = 0
                output += '/'
            if square == '':
                empties += 1
            else:
                if empties > 0:
                    output += str(empties)
                    empties = 0
                output += square
        if empties > 0:
            output += str(empties)
        return output

    def perform_move(self, start: int, end: int):
        color = color_of_piece(self.board[start])
        piece = self.board[start]
        captured_piece = None

        new_white_pieces = self.white_pieces.copy()
        new_black_pieces = self.black_pieces.copy()
        new_board = self.board.copy()

        new_board[start] = ''
        if new_board[end] != '':
            captured_piece = new_board[end]
        new_board[end] = piece
    
        if color == Color.black:
            new_black_pieces.append((piece, end))
            new_black_pieces.remove((piece, start))

            if captured_piece:
                new_white_pieces.remove((captured_piece.lower(), end))
        else:
            new_white_pieces.append((piece.lower(), end))
            new_white_pieces.remove((piece.lower(), start))
            if captured_piece:
                new_black_pieces.remove((captured_piece.lower(), end))

        return Position(self.board_height, self.board_width, new_board, new_white_pieces, new_black_pieces)

def color_of_piece(piece: str) -> Color:
    return Color.white if piece.isupper() else Color.black