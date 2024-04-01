from engine.board import Board
from engine.pieces import *
from engine.constants import *
from engine.utils import visualize_possible_moves
from engine.fen_utils import algebraic_to_coords
def main():
    board = Board()
    piece = 'g1'
    
    moves = board.get_possible_moves(piece)
    print(moves)
    visualize_possible_moves(moves, algebraic_to_coords(piece), 'p')
    p = board.get_piece(piece)
    print(p.get_color())

if __name__ == "__main__":
    main()