from chest import evaluate
from chest.models import Position, Color
from chest.evaluate import evaluate, alphabeta_max, next_position, next_position2
from chest.utils import open_fen
from math import inf

if __name__ == '__main__':
    position = Position.from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
    a, nextposition = next_position(position, Color.white, 6)
    print(a, nextposition)
    open_fen(str(nextposition))

    score, nextposition = next_position(nextposition, Color.black, 5)
    print(f"{position} -> {nextposition}")
    print(f"score: {score}")
    open_fen(str(nextposition))

    score, nextposition = next_position(nextposition, Color.white, 4)
    print(f"-> {nextposition}")
    print(nextposition)
    print(f"score: {score}")
    open_fen(str(nextposition))

    score, nextposition = next_position(nextposition, Color.black, 4)
    print(f"-> {nextposition}")
    print(nextposition)
    print(f"score: {score}")
    open_fen(str(nextposition))
 