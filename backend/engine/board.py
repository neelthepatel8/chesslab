from abc import ABC
from engine.constants import *
import engine.fen_utils as fen_utils
from engine.piece import Piece
from pprint import pprint
from engine.pieces import Pawn

class Board(ABC):
    def __init__(self, fen=START_FEN) -> None:
        super().__init__()
        self.fen = fen
        self.board = fen_utils.build_board_from_fen(fen)
        self.dead_pieces = {
            'black': [],
            'white': []
        }
        self.current_player = fen_utils.get_current_player(fen)
        self.halfmoves = fen_utils.get_halfmoves(fen)
        self.fullmoves = fen_utils.get_fullmoves(fen)
        self.castling_avalability = fen_utils.get_castling_avalability(fen)

    def make_fen(self):
        active = "w" if self.current_player == COLOR["WHITE"] else "b"
        castling = ''.join(self.castling_avalability)
        en_passant = '-'

        rows = []
        for row in self.board:
            fen_row = ""
            for piece in row:
                fen_row += piece.get_name() if isinstance(piece, Piece) else 'X'
            rows.append(fen_row)

        fen = '/'.join(rows)

        placements = fen_utils.make_compact(fen)
        all_fen = [placements, active, castling, en_passant, str(self.halfmoves), str(self.fullmoves)]
        self.fen = ' '.join(all_fen)

        print("New fen: ", self.fen)
        return self.fen

    def get_piece(self, piece_coords):
        rank, file = fen_utils.algebraic_to_coords(piece_coords)
        return self.board[rank - 1][file - 1]

    def get_possible_moves(self, piece_coords):
        rank, file = fen_utils.algebraic_to_coords(piece_coords)
        if not (1 <= rank <= 8 and 1 <= file <= 8):
            return None

        piece = self.board[rank - 1][file - 1]
        if not piece:
            return None

        all_paths = piece.get_possible_paths()
        valid_moves = []

        for path in all_paths:
            valid_path = []
            for r, f in path:
                if not (1 <= r <= 8 and 1 <= f <= 8):
                    break

                piece_at_pos = self.board[r - 1][f - 1]
                if piece_at_pos:
                    if piece_at_pos.get_color() == piece.get_color():
                        break
                    else:
                        if isinstance(piece, Pawn) and abs(piece.file - f) == 1:
                            if piece.can_move((r, f), is_capture=True):
                                valid_path.append((r, f))
                        elif not isinstance(piece, Pawn) or (isinstance(piece, Pawn) and abs(piece.file - f) == 1):
                            if piece.can_kill((r, f)):
                                valid_path.append((r, f))
                                break
                else:
                    if not isinstance(piece, Pawn) or (isinstance(piece, Pawn) and piece.file == f):
                        valid_path.append((r, f))

            valid_moves.extend(valid_path)

        if isinstance(piece, Pawn):
            final_valid_moves = []
            for move in valid_moves:
                r, f = move
                piece_at_target = self.board[r - 1][f - 1] if 1 <= r <= 8 and 1 <= f <= 8 else None
                if abs(piece.file - f) == 1 and piece_at_target and piece_at_target.get_color() != piece.get_color():
                    final_valid_moves.append(move)
                elif abs(piece.file - f) == 0 and not piece_at_target:
                    final_valid_moves.append(move)
            valid_moves = final_valid_moves

        return valid_moves



    def move_piece(self, from_pos, to_pos):
        if not from_pos or not to_pos: return ERROR_NO_POSITIONS_PROVIDED

        from_pos = fen_utils.algebraic_to_coords(from_pos)
        to_pos = fen_utils.algebraic_to_coords(to_pos)

        from_rank, from_file = from_pos
        to_rank, to_file = to_pos

        piece = self.board[from_rank - 1][from_file - 1]

        if not piece: return ERROR_NO_PIECE_TO_MOVE

        possible_moves = self.get_possible_moves(fen_utils.coords_to_algebraic(from_rank, from_file))
        if to_pos not in possible_moves: return ERROR_MOVE_NOT_POSSIBLE

        piece_at_pos = self.board[to_rank - 1][to_file - 1]
        
        if piece.get_color() == COLOR["BLACK"]:
            self.fullmoves += 1

        if not piece_at_pos:
            self.board[from_rank - 1][from_file - 1] = None
            self.board[to_rank - 1][to_file - 1] = piece
            piece.update_position(to_rank, to_file)
            self.current_player = COLOR["WHITE"] if self.current_player == COLOR["BLACK"] else COLOR["BLACK"]
            self.fen = self.make_fen()
            print("Updated board: ", self.fen)
            return SUCCESS_MOVE_MADE_NO_KILL

        self.dead_pieces[piece_at_pos.get_color()].append(piece_at_pos)
        self.board[from_rank - 1][from_file - 1] = None
        self.board[to_rank - 1][to_file - 1] = piece
        piece.update_position(to_rank, to_file)
        self.current_player = COLOR["WHITE"] if self.current_player == COLOR["BLACK"] else COLOR["BLACK"]
        self.halfmoves += 1
        self.fen = self.make_fen()
        print("Updated board: ", self.fen)

        return SUCCESS_MOVE_MADE_WITH_KILL