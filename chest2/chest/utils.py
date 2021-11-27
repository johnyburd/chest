from typing import Tuple
from urllib.parse import quote_plus
from webbrowser import open


def open_fen(fen: str):
    open("https://lichess.org/editor?fen=" + quote_plus(fen))


def raycast(pos, index: int, direction: Tuple[int, int], color, limit: int = -1, allow_capture: bool = True):
    if limit == 0:
        return ()
    next_index = index
    if index % pos.board_width == pos.board_width - 1 and direction[0] == 1:
        # we are moving into the right edge
        return ()

    if index % pos.board_width == 0 and direction[0] == -1:
        # we are moving into the left edge
        return ()

    if index >= (pos.board_width - 1) * pos.board_height and direction[1] == 1:
        # we are moving into the bottom
        return ()

    if index <= pos.board_width and direction[1] == -1:
        # we are moving into the top
        return ()

    # x component
    next_index += direction[0]
    # y component
    next_index += 8 * direction[1]

    if p := pos.board[next_index]:  # there is already a piece here
        if p.color == color or not allow_capture:
            return ()  # we can't move into our own team
        else:
            return (next_index,)  # if there's a guy here it's the last stop

    return (next_index,) + raycast(pos, next_index, direction, color, limit - 1)