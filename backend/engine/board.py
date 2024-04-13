from __future__ import annotations
from abc import ABC
import engine.constants as constants
import engine.fen_utils as fen_utils
from engine.piece import Piece
import engine.pieces as pieces
import copy
from engine.enpassant.EnPassantStatus import EnPassantStatus

from engine.Position import Position

class Board(ABC):
    def __init__(self, fen=constants.START_FEN) -> None:
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
        self.castling_availability = fen_utils.get_castling_availability(fen)
        
        self.is_stalemate = False
        self.is_checkmate = False 
        self.king_in_check = None
        
        self.all_legal_moves = {
            constants.COLOR["BLACK"]: [],
            constants.COLOR["WHITE"]: []
        }
        
        self.en_passant = EnPassantStatus()

    def make_fen(self):
        active = "w" if self.current_player == constants.COLOR["WHITE"] else "b"
        castling = ''.join(self.castling_availability) if len(self.castling_availability) > 0 else '-'

        en_passant = self.en_passant.eligible_square.algebraic if self.en_passant.available else '-'

        rows = []
        for rank in range(8):
            fen_row = ""
            empty_count = 0
            for file in range(8):
                position = Position(rank=rank + 1, file=file + 1)  
                piece = self.board[position.rank - 1][position.file - 1]  
                if isinstance(piece, Piece):
                    if empty_count > 0:
                        fen_row += str(empty_count)
                        empty_count = 0
                    fen_row += piece.get_name()
                else:
                    empty_count += 1
            if empty_count > 0:
                fen_row += str(empty_count)
            rows.append(fen_row)

        placements = '/'.join(rows)
        all_fen = [placements, active, castling, en_passant, str(self.halfmoves), str(self.fullmoves)]
        self.fen = ' '.join(all_fen)

        return self.fen


    def get_piece(self, position: Position):
        rank, file = position.rank, position.file
        return self.board[rank - 1][file - 1]
    
    def set_piece(self, position: Position, piece: Piece):
        rank, file = position.rank, position.file
        self.board[rank - 1][file - 1] = piece
    
    def clear_square(self, position: Position):
        self.set_piece(position, None)

    def get_pseudo_legal_moves(self, position: Position, simulate=False, log=False) -> list:
        if self.is_stalemate or self.is_checkmate: 
            return []
        
        rank, file = position.rank, position.file
        
        piece = self.get_piece(position)
        if not piece:
            return None

        all_paths = piece.get_possible_paths()
        valid_moves = []
        
        en_passant_added = None
        
        for path in all_paths:
            valid_path = []
            for pos in path:
                if not pos.is_on_board():
                    break

                piece_at_pos = self.get_piece(pos)

                if piece_at_pos:
                    if piece_at_pos.get_color() == piece.get_color():
                        break
                    else:
                        if isinstance(piece, pieces.Pawn) and abs(piece.position.file - pos.file) == 1:
                            if piece.can_move(pos, is_capture=True):
                                valid_path.append(pos)
                        elif not isinstance(piece, pieces.Pawn) or (isinstance(piece, pieces.Pawn) and abs(piece.position.file - pos.file) == 1):
                            if piece.can_kill(pos):
                                valid_path.append(pos)
                                break
                else:
                    if not self.king_in_check:
                        valid_moves.extend(self.get_castlable_moves(piece))
                    if not isinstance(piece, pieces.Pawn) or (isinstance(piece, pieces.Pawn) and piece.position.file == pos.file):
                        valid_path.append(pos)
                    
                    if not simulate:
                        if isinstance(piece, pieces.Pawn):
                            if self.en_passant.available and self.en_passant.pawn_color != piece.get_color():
                                possible = self.check_en_passant_possible_for_piece(piece)                                
                                if possible:
                                    valid_moves.append(self.en_passant.eligible_square)
                                    en_passant_added = self.en_passant.eligible_square

            valid_moves.extend(valid_path)
            
            
        if isinstance(piece, pieces.Pawn):
            final_valid_moves = []
            for move in valid_moves:
                piece_at_target = self.get_piece(move)
                if abs(piece.position.file - move.file) == 1 and piece_at_target and piece_at_target.get_color() != piece.get_color():
                    final_valid_moves.append(move)
                elif abs(piece.position.file - move.file) == 0 and not piece_at_target:
                    final_valid_moves.append(move)
            valid_moves = final_valid_moves

        if en_passant_added: 
            valid_moves.append(en_passant_added)
        return list(set(valid_moves))
    
    def get_all_pseudo_legal_moves(self, player: str, simulate=False) -> list:
        moves = []
        for row in self.board:
            for piece in row:
                if not piece: 
                    continue 
                if piece.get_color() != player: 
                    continue
                
                moves.extend(self.get_pseudo_legal_moves(piece.position, simulate))
        return list(set(moves)) 
    
    def deep_copy(self) -> Board:
        copy_board = Board(self.fen)
        copy_board.board = copy.deepcopy(self.board)
        copy_board.current_player = self.current_player
        copy_board.halfmoves = self.halfmoves
        copy_board.fullmoves = self.fullmoves
        copy_board.castling_availability = self.castling_availability
        copy_board.dead_pieces = copy.deepcopy(self.dead_pieces)
        return copy_board

    def is_move_legal(self, from_pos: Position, to_pos: Position) -> bool:
        board_copy = self.deep_copy()
        

        board_copy.move_piece(from_pos, to_pos, simulate=True)

        if board_copy.is_king_in_check(fen_utils.get_opposite_player(board_copy.current_player)):
            return False
        return True

    def get_legal_moves(self, position: Position, simulate=False, log=False) -> list:
        legal_moves = []
        pseudo_legal_moves = self.get_pseudo_legal_moves(position, simulate, log)
        for to_pos in pseudo_legal_moves:
            if self.is_move_legal(position, to_pos):
                legal_moves.append(to_pos)
        return list(set(legal_moves))
    
    def get_all_legal_moves(self, player: str, simulate: bool, log=False) -> list:
        moves = []
        for row in self.board:
            for piece in row:
                if not piece: 
                    continue 
                if piece.get_color() != player: 
                    continue
                moves.extend(self.get_legal_moves(piece.position, simulate, log))
        self.all_legal_moves[player] = moves
        return list(set(moves)) 

    def is_king_in_check(self, player: str) -> bool:
        king = self.get_king_location(player)
        all_possible_moves = self.get_all_pseudo_legal_moves(fen_utils.get_opposite_player(player), simulate=True)
        for move in all_possible_moves:
            if move == king:
                self.king_in_check = player
                return True

        self.king_in_check = None
        return False

    def get_king_location(self, player: str) -> Position:
        for row in self.board:
            for piece in row:
                if not piece: 
                    continue 
                if piece.get_color() != player: 
                    continue 
                if piece.get_name().lower() == 'k':
                    return piece.position
        
        return Position()
    
    def update_en_passant_status(self, from_pos: Position, to_pos: Position):
        from_rank, from_file = from_pos.rank, from_pos.file 
        to_rank, to_file = to_pos.rank, to_pos.file
        
        moved_piece = self.get_piece(to_pos)
        
        if isinstance(moved_piece, pieces.Pawn) and abs(to_rank - from_rank) == 2:
            eligible_square_rank = to_rank  + 1 if moved_piece.get_color() == constants.COLOR["WHITE"] else to_rank - 1
            eligible_square = Position(rank=eligible_square_rank, file=to_file)
            self.en_passant.set(eligible_square, to_pos, moved_piece.get_color())
        else:
            self.en_passant.clear()

    def check_en_passant_possible_for_piece(self, piece: Piece):
        piece_pos = piece.position
        rank, file = piece_pos.rank, piece_pos.file
        en_pass_position = self.en_passant.eligible_square
        en_pass_rank, en_pass_file = en_pass_position.rank, en_pass_position.file 
        
        if abs(rank - en_pass_rank) == 1 and abs(file - en_pass_file) == 1:
            if piece.get_color() == constants.COLOR["BLACK"]:
                return en_pass_rank > rank
            else:
                return rank > en_pass_rank
        else: 
            return False
    
    def move_piece(self, from_pos: Position, to_pos: Position, simulate=False):
        from_rank, from_file = from_pos.rank, from_pos.file
        to_rank, to_file = to_pos.rank, to_pos.file

        piece = self.get_piece(from_pos)
        piece_at_pos = self.get_piece(to_pos)

        if not piece: 
            return constants.ERROR_NO_PIECE_TO_MOVE
        
        if simulate:
            pseudo_legal_moves = self.get_pseudo_legal_moves(from_pos, simulate)
            if to_pos not in pseudo_legal_moves:
                return constants.ERROR_MOVE_NOT_POSSIBLE
        else:
            possible_moves = self.get_legal_moves(from_pos, simulate)
            if to_pos not in possible_moves:
                return constants.ERROR_MOVE_NOT_POSSIBLE


        if piece.get_color() == constants.COLOR["BLACK"]:
            self.fullmoves += 1

        if not piece_at_pos:
            
            has_castled = False
            if isinstance(piece, pieces.King) and abs(to_file - from_file) > 1 and not simulate:
                
                has_castled = self.castle(piece, from_pos, to_pos)
                if not has_castled: 
                    return constants.ERROR_MOVE_ILLEGAL_CASTLE
            
            has_en_passant = False
            if isinstance(piece, pieces.Pawn):
                if self.en_passant.available:
                    if self.check_en_passant_possible_for_piece(piece):
                        if to_pos == self.en_passant.eligible_square:
                            removed_pawn = self.get_piece(self.en_passant.target_pawn_position)
                            self.clear_square(self.en_passant.target_pawn_position)
                            self.dead_pieces[removed_pawn.get_color()].append(removed_pawn)
                            has_en_passant = True 
                            
            self.clear_square(from_pos)
            self.set_piece(to_pos, piece)
            piece.update_position(to_pos)
            self.current_player = constants.COLOR["WHITE"] if self.current_player == constants.COLOR["BLACK"] else constants.COLOR["BLACK"]
            self.update_castling_availability()
            if not simulate: 
                self.update_en_passant_status(from_pos, to_pos)
            self.fen = self.make_fen()
            
            
            if not simulate:
                
                if isinstance(piece, pieces.Pawn):
                    
                    if self.try_pawn_promote(to_pos, do_it=False) == constants.PAWN_CAN_PROMOTE:
                        return constants.SUCCESS_MOVE_MADE_NO_KILL_PROMOTE_POSSIBLE
                    
                if self.is_game_over(simulate):
                    return constants.SUCCESS_MOVE_MADE_NO_KILL_CHECKMATE if self.is_checkmate else constants.SUCCESS_MOVE_MADE_NO_KILL_STALEMATE
                
                if self.is_king_in_check(self.current_player): 
                    return constants.SUCCESS_MOVE_MADE_NO_KILL_CHECK if not has_castled else constants.SUCCESS_MOVE_MADE_NO_KILL_CHECK_CASTLED
            
            if has_castled:
                return constants.SUCCESS_MOVE_MADE_NO_KILL_NO_CHECK_CASTLED

            if has_en_passant:
                return constants.SUCCESS_MOVE_MADE_WITH_KILL_NO_CHECK 
            
            return constants.SUCCESS_MOVE_MADE_NO_KILL_NO_CHECK

        self.clear_square(from_pos)
        self.set_piece(to_pos, piece)
        piece.update_position(to_pos)
        self.current_player = constants.COLOR["WHITE"] if self.current_player == constants.COLOR["BLACK"] else constants.COLOR["BLACK"]
        self.halfmoves += 1
        self.update_castling_availability()
        if not simulate: 
            self.update_en_passant_status(from_pos, to_pos)
        self.fen = self.make_fen()
        
        
        if not simulate:
            
            if isinstance(piece, pieces.Pawn):
                if self.try_pawn_promote(to_pos, do_it=False) == constants.PAWN_CAN_PROMOTE:
                    return constants.SUCCESS_MOVE_MADE_WTIH_KILL_PROMOTE_POSSIBLE
        
            if self.is_game_over(simulate):
                return constants.SUCCESS_MOVE_MADE_WITH_KILL_CHECKMATE if self.is_checkmate else constants.SUCCESS_MOVE_MADE_WITH_KILL_STALEMATE
            
            if self.is_king_in_check(self.current_player): 
                return constants.SUCCESS_MOVE_MADE_WITH_KILL_CHECK
            
        return constants.SUCCESS_MOVE_MADE_WITH_KILL_NO_CHECK
    
    def get_castlable_moves(self, piece):
        moves = []
            
        if isinstance(piece, pieces.King):
            if piece.get_color() == constants.COLOR["WHITE"]:
                if 'K' in self.castling_availability:
                    to_append = True
                    pieces_in_middle = ['f1', 'g1']
                    for p in pieces_in_middle:
                        r, f = fen_utils.algebraic_to_coords(p)
                        if self.board[r - 1][f - 1]:
                            to_append = False
                            break
                        if self.is_targeted_square(p):
                            to_append = False
                            break
                    if to_append: 
                            moves.append(Position(algebraic='g1'))
                if 'Q' in self.castling_availability:
                    to_append = True
                    pieces_in_middle = ['b1', 'c1', 'd1']
                    for p in pieces_in_middle:
                        r, f = fen_utils.algebraic_to_coords(p)
                        if self.board[r - 1][f - 1]:
                            to_append = False
                            break
                        if self.is_targeted_square(p):
                            to_append = False
                            break
                    if to_append: 
                        moves.append(Position(algebraic='c1'))
            elif piece.get_color() == constants.COLOR["BLACK"]:
                if 'k' in self.castling_availability:
                    to_append = True
                    pieces_in_middle = ['f8', 'g8']
                    for p in pieces_in_middle:
                        r, f = fen_utils.algebraic_to_coords(p)
                        if self.board[r - 1][f - 1]:
                            to_append = False
                            break
                        if self.is_targeted_square(p):
                            to_append = False
                            break
                    if to_append: 
                        moves.append(Position(algebraic='g8'))
                if 'q' in self.castling_availability:
                    to_append = True
                    pieces_in_middle = ['b8', 'c8', 'd8']
                    for p in pieces_in_middle:
                        r, f = fen_utils.algebraic_to_coords(p)
                        if self.board[r - 1][f - 1]:
                            to_append = False
                            break
                        if self.is_targeted_square(p):
                            to_append = False
                            break
                    if to_append: 
                            moves.append(Position(algebraic='c8'))
        return moves
    
    def is_targeted_square(self, position: Position):
        player = fen_utils.get_opposite_player(self.current_player)
        legal_moves = self.all_legal_moves[player]
        return position in legal_moves
    
    def castle(self, piece: Piece, from_pos: Position, to_pos: Position):
        print("CASTLING")
        
        if self.is_king_in_check(self.current_player):
            print("King in check!")
            return False
        
        self.update_castling_availability()
        if not self.castling_availability:
            print("Castling not available")
            return False
        
        if to_pos.file > from_pos.file:
            castling = 'k' if piece.get_color() == constants.COLOR["BLACK"] else "K"
        elif from_pos.file > to_pos.file:
            castling = 'q' if piece.get_color() == constants.COLOR["BLACK"] else 'Q'
            
        if castling not in self.castling_availability:
            print("Reached here!")
            
            return False 
    
        if castling in 'kK':
            if castling == 'k': 
                pos1, pos2 = Position(algebraic='h8'), Position(algebraic='f8')
            else: 
                pos1, pos2 = Position(algebraic='h1'), Position(algebraic='f1')
        else:
            if castling == 'q': 
                pos1, pos2 = Position(algebraic='a8'), Position(algebraic='d8')
            else: 
                pos1, pos2 = Position(algebraic='a1'), Position(algebraic='d1')

        print("Reached here!")
        if pos1.is_on_board() and pos2.is_on_board():
            rook = self.get_piece(pos1)
            self.set_piece(pos2, rook)
            self.clear_square(pos1)
            rook.update_position(pos2)
            return True
        return False 
    
    def update_castling_availability(self):
        self.castling_availability = ''
        
        def is_rook_ready_for_castling(piece, expected_name):
            return piece is not None and piece.get_name() == expected_name and not piece.has_moved

        def is_king_ready_for_castling(piece, expected_name):
            return piece is not None and piece.get_name() == expected_name and not piece.has_moved
        
        if is_king_ready_for_castling(self.board[7][4], 'K'):
            if is_rook_ready_for_castling(self.board[7][0], 'R'):
                self.castling_availability += 'Q'
            if is_rook_ready_for_castling(self.board[7][7], 'R'):
                self.castling_availability += 'K'
        
        if is_king_ready_for_castling(self.board[0][4], 'k'):
            if is_rook_ready_for_castling(self.board[0][0], 'r'):
                self.castling_availability += 'q'
            if is_rook_ready_for_castling(self.board[0][7], 'r'):
                self.castling_availability += 'k'

    def is_game_over(self, simulate=False):
        all_legal_moves = self.get_all_legal_moves(self.current_player, simulate, log=False)
        if len(all_legal_moves) == 0 or self.are_only_kings_on_board():
            king_check = self.is_king_in_check(self.current_player)
            if king_check:
                self.is_checkmate = True 
            else:
                self.is_stalemate = True
                
        return self.is_stalemate or self.is_checkmate
    
    def are_only_kings_on_board(self):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece: 
                    pieces.append(piece)
                
        are_kings_only = True
        for piece in pieces:
            if piece.get_name().lower() != "k":
                are_kings_only = False

        return are_kings_only    
    
    def try_pawn_promote(self, position: Position, promote_to="queen", do_it=False):
        rank, file = position.rank, position.file
        piece = self.get_piece(position)
        final_rank = constants.MAX_RANK if piece.get_color() == constants.COLOR["BLACK"] else constants.MIN_RANK 

        can_promote = rank == final_rank
        if not do_it: 
            if can_promote: 
                return constants.PAWN_CAN_PROMOTE
            else: 
                return constants.PAWN_CANNOT_PROMOTE  
       
        if can_promote:
            promoted_piece = self.make_promotion_piece(promote_to, position, piece.get_color())
            self.set_piece(position, promoted_piece)
            self.fen = self.make_fen()   
            if self.is_game_over():
                return constants.SUCCESS_PAWN_PROMOTED_CHECKMATE if self.is_checkmate else constants.SUCCESS_PAWN_PROMOTED_STALEMATE
            
            if self.is_king_in_check(self.current_player):
                return constants.SUCCESS_PAWN_PROMOTED_CHECK
        return constants.SUCCESS_PAWN_PROMOTED
        
    def make_promotion_piece(self, piece_type: str, position: Position, color: str):
        if piece_type == "queen":
            return pieces.Queen(position, color)
        
        if piece_type == "rook":
            return pieces.Rook(position, color)

        if piece_type == "knight":
            return pieces.Knight(position, color)
        
        if piece_type == "bishop":
            return pieces.Bishop(position, color)