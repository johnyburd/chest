from enum import Enum
from typing import List, Tuple, Optional
from copy import deepcopy
from dataclasses import dataclass
from itertools import chain
from functools import lru_cache

from chest.utils import raycast

straight_directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
diagonal_directions = ((1, 1), (-1, 1), (1, -1), (-1, -1))

class Color(Enum):
    white = 1
    black = 2

    def __invert__(self):
        if self == Color.white:
            return Color.black
        return Color.white

class Chessman(str, Enum):
    king = 'k'
    queen = 'q'
    knight = 'n'
    rook = 'r'
    pawn = 'p'
    bishop = 'b'

class Piece:

    value = 0

    @classmethod
    def from_char(cls, c: str, idx: int) -> 'Piece':
        color = Color.black
        if c.isupper():
            color = Color.white
        type = c.lower()
        if type == Chessman.king:
            return King(color, type, idx)
        elif type == Chessman.queen:
            return Queen(color, type, idx)
        elif type == Chessman.rook:
            return Rook(color, type, idx)
        elif type == Chessman.bishop:
            return Bishop(color, type, idx)
        elif type == Chessman.knight:
            return Knight(color, type, idx)
        elif type == Chessman.pawn:
            return Pawn(color, type, idx)

    def __init__(self, color: Color, type: Chessman, index: int):
        self.color = color
        self.type = type
        self.index = index

    @property
    def is_white(self):
        return self.color == Color.white

    def move(self, index: int) -> 'Piece':
        return self.__class__(self.color, self.type, index)

    def get_moves(self, pos: 'Position'):
        raise NotImplementedError

    def __str__(self):
        if self.color == Color.white:
            return self.type.upper()
        return self.type
    
    def __hash__(self):
        return hash(str(self) + str(self.index))

class King(Piece):
    def get_moves(self, pos: 'Position'):
        return chain(*(raycast(pos, self.index, v, self.color, limit=1) for v in straight_directions + diagonal_directions))

class Queen(Piece):
    value = 9
    def get_moves(self, pos: 'Position'):
        return chain(*(raycast(pos, self.index, v, self.color) for v in straight_directions + diagonal_directions))

class Rook(Piece):
    value = 5
    def get_moves(self, pos: 'Position'):
        return chain(*(raycast(pos, self.index, v, self.color) for v in straight_directions))

class Bishop(Piece):
    value = 3
    def get_moves(self, pos: 'Position'):
        return chain(*(raycast(pos, self.index, v, self.color) for v in diagonal_directions))

class Knight(Piece):
    value = 3
    def get_moves(self, pos: 'Position'):
        return ()


class Pawn(Piece):
    value = 1
    def get_moves(self, pos: 'Position'):
        if self.color == Color.white:
            starting_pos = self.index <= 55 and self.index >= 48
            direction = (0, -1)
        else:
            starting_pos = self.index <= 15 and self.index >= 8
            direction = (0, 1)
        limit = 2 if starting_pos else 1
        return raycast(pos, self.index, direction, self.color, limit=limit, allow_capture=False)

class Position:
    def __init__(self, height: int, width: int, board: List[Optional[Piece]]):
        self.board_height = height 
        self.board_width = width
        self.board = board

    @property
    def white_pieces(self):
        return (p for p in self.board if p is not None and p.is_white)

    @property
    def black_pieces(self):
        return (p for p in self.board if p is not None and not p.is_white)

    def __hash__(self):
        return hash(''.join(str(s) for s in self.board))

    @classmethod
    def from_fen(self, fen: str) -> 'Position':
        position = Position(8, 8, [None for _ in range(8*8)])
        rows = fen.split('/')
        row_idx = 0
        for row in rows:
            column = 0
            for c in row:
                if c.isnumeric():
                    column += int(c) - 1
                else:
                    idx = position.board_width * row_idx + column
                    position.board[idx] = Piece.from_char(c, idx)
                column += 1
            row_idx += 1
        return position
        
    def to_fen(self) -> str:
        output = ''
        empties = 0
        for i, square in enumerate(self.board):
            if i % self.board_width == 0 and i > 0:
                if empties > 0:
                    output += str(empties)
                    empties = 0
                output += '/'
            if square is None:
                empties += 1
            else:
                if empties > 0:
                    output += str(empties)
                    empties = 0
                output += str(square)
        if empties > 0:
            output += str(empties)
        return output

    def perform_move(self, piece: Piece, end: int):
        new_board = deepcopy(self.board)
        new_piece = piece.move(end)

        new_board[end] = new_piece
        new_board[piece.index] = None

        return Position(self.board_height, self.board_width, new_board)

    def get_children(self, color: Color):
        for piece in (p for p in self.board if p is not None and p.color == color):
            moves = piece.get_moves(self)
            for move in moves:
                yield self.perform_move(piece, move)
    
    def __str__(self):
        return self.to_fen()