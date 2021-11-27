from dataclasses import astuple
from chest.models import Piece, Position, Color, piece_values
from chest.utils import color_of_piece, calculate_moves
from math import inf
from datetime import datetime
from collections import Counter
from functools import lru_cache

def alpha_beta(pos: Position, counter: Counter, black: bool = False, max_depth: int = 3, depth: int = 0, alpha: float = -inf, beta: float = inf, maxing: bool = True):
    if depth == max_depth:
        return None, evaluate(pos, black)

    if counter['pos'] % 1000 == 0:
        print(f"evaluated {counter['pos']} positions")

    board = evaluate(pos, black)
    if board == inf or board == -inf:

        return None, board

    if black:
        pieces = pos.black_pieces if maxing else pos.white_pieces
    else:
        pieces = pos.white_pieces if maxing else pos.black_pieces
    comparator = (lambda a, v: v > a) if maxing else (lambda b, v: v < b)

    best_move = (0, 0)

    #print(pieces)
    value = -inf if maxing else inf

    for p, idx in pieces:
        moves = calculate_moves(pos, idx)
        #print(f"{p} has these moves: {moves}")
        positions = [(pos.perform_move(idx, move), move) for move in moves]
        counter['pos'] += len(positions)
        for new_pos, move in positions:

            _, new_val = alpha_beta(new_pos, counter, black, max_depth, depth + 1, alpha, beta, not maxing)
            #if move == 41:
                #print(comparator(1, 2), maxing)
                #print(f"{depth}: {new_pos.to_fen()}, new_val {new_val} eval: {evaluate(new_pos, black)}")
            if comparator(value, new_val):
                value = new_val

            if maxing:
                #print(f"compare {alpha} to {value}")
                if value >= beta:
                    break
                if comparator(alpha, value):
                    alpha = value
                    #print(f"best_move {new_pos.to_fen()} rated {alpha} eval {evaluate(new_pos, black)}")
                    best_move = (idx, move)
                    if alpha == inf:
                        print(new_pos.to_fen())
                        print("hi")
                        return best_move, alpha
            else:
                if value <= alpha:
                    break
                if comparator(beta, value):
                    beta = value
    return best_move, value


def find_best_move(pos: Position, turn: Color, max_depth: int = 5):
    now = datetime.now()
    c = Counter()
    move, score = alpha_beta(pos, c, turn == Color.black, max_depth)
    print(f"time: {datetime.now() - now}")
    return move[0], move[1]

def evaluate(pos: Position, black: bool = False):
    return _evaluate(pos) * (-1 if black else 1)
@lru_cache(maxsize=6_000_000)
def _evaluate(pos: Position):
    # check checks
    
    white_king_idx = next((p[1] for p in pos.white_pieces if p[0] == Piece.king), None)
    if white_king_idx is None:
        return - inf
    black_king_idx = next((p[1] for p in pos.black_pieces if p[0] == Piece.king), None)
    if black_king_idx is None:
        return inf

    white_in_check = in_check(pos, white_king_idx)
    black_in_check = in_check(pos, black_king_idx)

    white_king_moves = calculate_moves(pos, white_king_idx)
    black_king_moves = calculate_moves(pos, black_king_idx)

    if len(white_king_moves) == 0 and white_in_check:
        return - inf
    if len(black_king_moves) == 0 and black_in_check:
        return inf

    return score_pieces(pos)


def score_pieces(pos: Position) -> int:
    # TODO scale by number of remaining pieces
    white_score = sum(piece_values[Piece(p[0])] for p in pos.white_pieces)
    black_score = sum(piece_values[Piece(p[0])] for p in pos.black_pieces)
    return white_score - black_score

@lru_cache(maxsize=6_000_000)
def in_check(position: Position, king_idx: int):
    color = color_of_piece(position.board[king_idx])
    pieces = position.white_pieces if color == Color.black else position.black_pieces
    for _, idx in pieces:
        if king_idx in calculate_moves(position, idx):
            return True
    return False