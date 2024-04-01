from abc import ABC
from engine.constants import *
import engine.fen_utils as fen_utils
from engine.piece import Piece

class Board(ABC):
    def __init__(self, fen=START_FEN) -> None:
        super().__init__()
        self.fen = fen
        self.board = fen_utils.build_board_from_fen(fen)

    def make_fen(self):
        active = 'b'
        castling = '-'
        en_passant = '-'
        halfmove = '0'
        full_move = '0'

        rows = []
        for row in self.board:
            fen_row = ""
            for piece in row:
                fen_row += piece.get_name() if isinstance(piece, Piece) else 'X'
            rows.append(fen_row)

        fen = '/'.join(rows)

        placements = fen_utils.make_compact(fen)
        all_fen = [placements, active, castling, en_passant, halfmove, full_move]
        return ' '.join(all_fen)

    def get_piece(self, piece_coords):
        rank, file = fen_utils.algebraic_to_coords(piece_coords)
        return self.board[rank - 1][file - 1]
    
    def get_possible_moves(self, piece_coords):
        rank, file = fen_utils.algebraic_to_coords(piece_coords)
        piece = self.board[rank - 1][file - 1]

        if not piece:
            return None

        all_paths = piece.get_possible_paths()
        print(all_paths)
        print("All paths: ", [[fen_utils.coords_to_algebraic(r, f) for r, f in path] for path in all_paths], " for: ", piece_coords)

        valid_moves = []
        for path in all_paths:
            for r, f in path:
                piece_at_pos = self.board[r - 1][f - 1]
                if piece_at_pos:
                    if piece_at_pos.get_color() != piece.get_color():
                        valid_moves.append((r, f))
                    break
                else:
                    valid_moves.append((r, f))

        return valid_moves
