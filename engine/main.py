from board import Board
from pieces import *
from constants import *
from utils import visualize_possible_moves
from fen_utils import algebraic_to_coords
def main():
    board = Board()
    piece = 'e1'
    moves = board.get_possible_moves(piece)
    visualize_possible_moves(moves, algebraic_to_coords(piece), 'p')

if __name__ == "__main__":
    main()