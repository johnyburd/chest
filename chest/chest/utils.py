from chest.models import Color, Position, Piece
from typing import List, Tuple
from urllib.parse import quote_plus
from webbrowser import open
from functools import lru_cache


def open_fen(fen: str):
    open("https://lichess.org/editor?fen=" + quote_plus(fen))

def color_of_piece(piece: str) -> Color:
    return Color.white if piece.isupper() else Color.black

@lru_cache(maxsize=6_000_000)
def calculate_moves(position: Position, index: int) -> List[int]:
    piece = position.board[index].lower()
    color = color_of_piece(position.board[index])

    moves = ()
    if piece == Piece.king:
        for i in range (-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                moves += raycast(position, index, (i, j), color, 1)
    elif piece == Piece.queen:
        for i in range (-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                moves += raycast(position, index, (i, j), color)
    elif piece == Piece.rook:
        moves += raycast(position, index, (1, 0), color)
        moves += raycast(position, index, (-1, 0), color)
        moves += raycast(position, index, (0, 1), color)
        moves += raycast(position, index, (0, -1), color)

    elif piece == Piece.bishop:
        moves += raycast(position, index, (1, 1), color)
        moves += raycast(position, index, (-1, 1), color)
        moves += raycast(position, index, (-1, -1), color)
        moves += raycast(position, index, (1, -1), color)
    elif piece == Piece.knight:
        pass
    elif piece == Piece.pawn:
        pass
    return moves

def raycast(pos: Position, index: int, direction: Tuple[int, int], color: Color, limit: int = 0, step: int = 0):
    if limit != 0 and step >= limit:
        return ()
    next_index = index
    if index % pos.board_width == pos.board_width - 1 and direction[0] == 1:  # we are at the right edge
        return ()

    if index % pos.board_width == 0 and direction[0] == -1:  # we are at the leftmost edge
        return ()

    if index >= (pos.board_width - 1) * pos.board_height and direction[1] == 1:  # we are moving into the bottom
        return ()

    if index <= pos.board_width and direction[1] == -1:  # we are moving into the top
        return ()

    # x component
    next_index += direction[0]
    # y component
    next_index += 8 * direction[1]

    if p := pos.board[next_index]:  # there is already a piece here
        if color_of_piece(p) == color:
            return ()  # we can't move into our own team
        else:
            return (next_index,)  # if there's a guy here it's the last stop

    return (next_index,) + raycast(pos, next_index, direction, color, limit, step + 1)