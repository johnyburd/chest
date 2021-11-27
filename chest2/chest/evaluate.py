from chest.models import Position, Chessman, Piece, Color
from math import inf
from functools import lru_cache
from datetime import datetime


def alphabeta_max(pos: Position, alpha: float, beta: float, depth: int):
    if depth == 0:
       return evaluate(pos, False)
    for child in pos.get_children(Color.white):
        score = alphabeta_min(child, alpha, beta, depth - 1)
        if score >= beta:
            return beta   # fail hard beta-cutoff
        if score > alpha:
            alpha = score # alpha acts like max in MiniMax
    return alpha

def alphabeta_min(pos: Position, alpha: float, beta: float, depth: int):
    if depth == 0:
        return -evaluate(pos, False)
    for child in pos.get_children(Color.black):
        score = alphabeta_max(child, alpha, beta, depth - 1)
        if score <= alpha:
            return alpha # fail hard alpha-cutoff
        if score < beta:
            beta = score  # beta acts like min in MiniMax
    return beta

def next_position2(pos: Position, color: Color, depth=3):

    best = None
    highscore = -inf
    for child in pos.get_children(Color.white):
        score = alphabeta_min(child, -inf, inf, depth)
        if score > highscore:
            highscore = score
            best = child
    return highscore, best


def next_position(pos, color: Color, depth=3):
    now = datetime.now()
    best_pos = pos
    best_score = -inf
    best_depth = 0
    for child in pos.get_children(color):
        score, child_depth = alpha_beta(child, ~color, color == Color.black, depth, maximizing=False)
        print(child, score, child_depth)
        if score > best_score:
            best_pos = child
            best_score = score
        elif score == best_score and child_depth >= best_depth:
            best_depth = child_depth
            best_pos = child
            best_score = score

    print(f"CHOSE {best_pos} {best_score} {best_depth} in {datetime.now() - now}")
    return best_score, best_pos

def alpha_beta(pos: Position, color: Color, for_black: bool, depth: int, a: float = -inf, b: float = inf, maximizing: bool = True):
    pos_score = evaluate(pos, for_black)
    if depth == 0 or pos_score in (inf, -inf):
        return pos_score, depth

    sol_depth = 0
    if maximizing:
        val = -inf
        for child in pos.get_children(color):
            new_val, new_sol_depth = alpha_beta(child, ~color, for_black, depth - 1, a, b, False)
            sol_depth = max(sol_depth, new_sol_depth)
            val = max(val, new_val)
            if val >= b:
                break
            if val > a:
                a = val
        return val, sol_depth
    else:
        val = inf
        for child in pos.get_children(color):
            new_val, new_sol_depth = alpha_beta(child, ~color, for_black, depth - 1, a, b, True)
            sol_depth = max(sol_depth, new_sol_depth)
            val = min(val, new_val)
            if val <= a:
                break
            if val < b:
                b = val
        return val, sol_depth


def evaluate(pos: Position, black: bool = False):
    return _evaluate(pos) * (-1 if black else 1)

#@lru_cache(maxsize=None)
def _evaluate(pos: Position):
    # check checks
    
    white_king = next((p for p in pos.white_pieces if p.type == Chessman.king), None)
    if white_king is None:
        return - inf
    black_king = next((p for p in pos.black_pieces if p.type == Chessman.king), None)
    if black_king is None:
        return inf

    white_in_check = in_check(pos, white_king)
    black_in_check = in_check(pos, black_king)

    if len(tuple(white_king.get_moves(pos))) == 0 and white_in_check:
        return - inf
    if len(tuple(black_king.get_moves(pos))) == 0 and black_in_check:
        return inf

    bonus = 0

    return score_pieces(pos) + bonus


def score_pieces(pos: Position) -> int:
    # TODO scale by number of remaining pieces
    white_score = sum(p.value for p in pos.white_pieces)
    black_score = sum(p.value for p in pos.black_pieces)
    return white_score - black_score



def in_check(position: Position, king: Piece):
    pieces = position.black_pieces if king.is_white else position.white_pieces
    for piece in pieces:
        if king.index in piece.get_moves(position):
            return True
    return False