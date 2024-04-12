from abc import ABC
import engine.constants as constants
import engine.fen_utils as fen_utils
from engine.piece import Piece
import engine.pieces as pieces
import copy
from engine.enpassant.EnPassantStatus import EnPassantStatus

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
        en_passant = self.en_passant.eligible_square if self.en_passant.available else '-'

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

        return self.fen

    def get_piece(self, piece_coords):
        rank, file = fen_utils.algebraic_to_coords(piece_coords)
        return self.board[rank - 1][file - 1]

    def get_pseudo_legal_moves(self, piece_coords, simulate=False, log=False):
        if self.is_stalemate or self.is_checkmate: 
            return []
        
        rank, file = fen_utils.algebraic_to_coords(piece_coords)
        if not (1 <= rank <= 8 and 1 <= file <= 8):
            return None

        piece = self.board[rank - 1][file - 1]
        if not piece:
            return None

        all_paths = piece.get_possible_paths()
        valid_moves = []
        

        en_passant_added = None
        
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
                        if isinstance(piece, pieces.Pawn) and abs(piece.file - f) == 1:
                            if piece.can_move((r, f), is_capture=True):
                                valid_path.append((r, f))
                        elif not isinstance(piece, pieces.Pawn) or (isinstance(piece, pieces.Pawn) and abs(piece.file - f) == 1):
                            if piece.can_kill((r, f)):
                                valid_path.append((r, f))
                                break
                else:
                    if not self.king_in_check:
                        valid_moves.extend(self.get_castlable_moves(piece))
                    if not isinstance(piece, pieces.Pawn) or (isinstance(piece, pieces.Pawn) and piece.file == f):
                        valid_path.append((r, f))
                    
                    if not simulate:
                        if isinstance(piece, pieces.Pawn):
                            if self.en_passant.available and self.en_passant.pawn_color != piece.get_color():
                                if log: 
                                    print("En passant available ", self.en_passant.eligible_square, self.en_passant.pawn_color)
                                possible = self.check_en_passant_possible_for_piece(piece)                                
                                if possible:
                                    move = fen_utils.algebraic_to_coords(self.en_passant.eligible_square)
                                    if log: 
                                        print("En passant Possible adding move: ", self.en_passant.eligible_square) 
                                    valid_moves.append(move)
                                    en_passant_added = move
                            else:
                                if log: 
                                    print("En passant not available")

            valid_moves.extend(valid_path)
        if log: 
            print(fen_utils.algebraic_list(valid_moves))
        if isinstance(piece, pieces.Pawn):
            final_valid_moves = []
            for move in valid_moves:
                r, f = move
                piece_at_target = self.board[r - 1][f - 1] if 1 <= r <= 8 and 1 <= f <= 8 else None
                if abs(piece.file - f) == 1 and piece_at_target and piece_at_target.get_color() != piece.get_color():
                    final_valid_moves.append(move)
                elif abs(piece.file - f) == 0 and not piece_at_target:
                    final_valid_moves.append(move)
            valid_moves = final_valid_moves

        if en_passant_added: 
            valid_moves.append(en_passant_added)
        return list(set(valid_moves))
    
    def get_all_pseudo_legal_moves(self, player, simulate=False):
        moves = []
        for row in self.board:
            for piece in row:
                if not piece: 
                    continue 
                if piece.get_color() != player: 
                    continue
                moves.extend(self.get_pseudo_legal_moves(piece.get_algebraic_pos(), simulate))
        return list(set(moves)) 
    
    def deep_copy(self):
        copy_board = Board(self.fen)
        copy_board.board = copy.deepcopy(self.board)
        copy_board.current_player = self.current_player
        copy_board.halfmoves = self.halfmoves
        copy_board.fullmoves = self.fullmoves
        copy_board.castling_availability = self.castling_availability
        copy_board.dead_pieces = copy.deepcopy(self.dead_pieces)
        return copy_board

    def is_move_legal(self, from_pos, to_pos):
        board_copy = self.deep_copy()

        board_copy.move_piece(from_pos, to_pos, simulate=True)

        if board_copy.is_king_in_check(fen_utils.get_opposite_player(board_copy.current_player)):
            return False
        return True

    def get_legal_moves(self, piece_coords, simulate=False, log=False):
        legal_moves = []
        pseudo_legal_moves = self.get_pseudo_legal_moves(piece_coords, simulate, log)
        for rank, file in pseudo_legal_moves:
            to_algebraic = fen_utils.coords_to_algebraic(rank, file)
            if self.is_move_legal(piece_coords, to_algebraic):
                legal_moves.append((rank, file))
        return list(set(legal_moves))
    
    def get_all_legal_moves(self, player, simulate, log=False):
        moves = []
        for row in self.board:
            for piece in row:
                if not piece: 
                    continue 
                if piece.get_color() != player: 
                    continue
                moves.extend(self.get_legal_moves(piece.get_algebraic_pos(), simulate, log))
        self.all_legal_moves[player] = moves
        return list(set(moves)) 

    def is_king_in_check(self, player):
        king = self.get_king_location(player)
        all_possible_moves = self.get_all_pseudo_legal_moves(fen_utils.get_opposite_player(player), simulate=True)
        for move in all_possible_moves:
            if move == king:
                self.king_in_check = player
                return True

        self.king_in_check = None
        return False

    def get_king_location(self, player):
        for row in self.board:
            for piece in row:
                if not piece: 
                    continue 
                if piece.get_color() != player: 
                    continue 
                if piece.get_name().lower() == 'k':
                    return piece.rank, piece.file
        
        return -1, -1
    
    def update_en_passant_status(self, from_pos, to_pos):
        print(f"Checking en passant status {from_pos} - {to_pos}")
        from_rank, from_file = fen_utils.algebraic_to_coords(from_pos)
        to_rank, to_file = fen_utils.algebraic_to_coords(to_pos)
        moved_piece = self.board[to_rank - 1][to_file - 1]
        
        print("Moving piece: ", to_rank, to_file)
        if isinstance(moved_piece, pieces.Pawn) and abs(to_rank - from_rank) == 2:
            eligible_square_rank = to_rank  + 1 if moved_piece.get_color() == constants.COLOR["WHITE"] else to_rank - 1
            print(eligible_square_rank, to_file)
            eligible_square = fen_utils.coords_to_algebraic(eligible_square_rank, to_file)
            print("Eligible! ", eligible_square)
            self.en_passant.set(eligible_square, to_pos, moved_piece.get_color())
        else:
            self.en_passant.clear()

    def check_en_passant_possible_for_piece(self, piece):
        rank, file = piece.rank, piece.file
        en_pas_rank, en_pas_file = fen_utils.algebraic_to_coords(self.en_passant.eligible_square)
        
        if abs(rank - en_pas_rank) == 1 and abs(file - en_pas_file) == 1:
            if piece.get_color() == constants.COLOR["BLACK"]:
                return en_pas_rank > rank
            else:
                return rank > en_pas_rank
        else: 
            return False
    
    def move_piece(self, from_pos, to_pos, simulate=False):
        if not from_pos or not to_pos: 
            return constants.ERROR_NO_POSITIONS_PROVIDED

        alg_from_pos = from_pos
        alg_to_pos = to_pos 
        
        from_pos = fen_utils.algebraic_to_coords(from_pos)
        to_pos = fen_utils.algebraic_to_coords(to_pos)

        from_rank, from_file = from_pos
        to_rank, to_file = to_pos

        piece = self.get_piece(from_pos)
        piece_at_pos = self.get_piece(to_pos)

        if not piece: 
            return constants.ERROR_NO_PIECE_TO_MOVE
        
        if simulate:
            pseudo_legal_moves = self.get_pseudo_legal_moves(alg_from_pos, simulate)
            if to_pos not in pseudo_legal_moves:
                return constants.ERROR_MOVE_NOT_POSSIBLE
        else:
            possible_moves = self.get_legal_moves(alg_from_pos, simulate)
            if to_pos not in possible_moves:
                return constants.ERROR_MOVE_NOT_POSSIBLE


        if piece.get_color() == constants.COLOR["BLACK"]:
            self.fullmoves += 1

        if not piece_at_pos:
            
            has_castled = False
            if isinstance(piece, pieces.King) and abs(to_pos[1] - from_pos[1]) > 1 and not simulate:
                
                has_castled = self.castle(piece, from_pos, to_pos)
                if not has_castled: 
                    return constants.ERROR_MOVE_ILLEGAL_CASTLE
            
            has_en_passant = False
            if isinstance(piece, pieces.Pawn):
                if self.en_passant.available:
                    if self.check_en_passant_possible_for_piece(piece):
                        if fen_utils.coords_to_algebraic(to_rank, to_file) == self.en_passant.eligible_square:
                            target_rank, target_file = fen_utils.algebraic_to_coords(self.en_passant.target_pawn_position)
                            removed_pawn = self.board[target_rank - 1][target_file - 1]
                            self.board[target_rank - 1][target_file - 1] = None 
                            self.dead_pieces[removed_pawn.get_color()].append(removed_pawn)
                            has_en_passant = True 
                            
            self.board[from_rank - 1][from_file - 1] = None
            self.board[to_rank - 1][to_file - 1] = piece
            piece.update_position(to_rank, to_file)
            self.current_player = constants.COLOR["WHITE"] if self.current_player == constants.COLOR["BLACK"] else constants.COLOR["BLACK"]
            self.update_castling_availability()
            if not simulate: 
                self.update_en_passant_status(alg_from_pos, alg_to_pos)
            self.fen = self.make_fen()
            
            
            if not simulate:
                
                if isinstance(piece, pieces.Pawn):
                    
                    if self.try_pawn_promote(alg_to_pos, do_it=False) == constants.PAWN_CAN_PROMOTE:
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

        self.dead_pieces[piece_at_pos.get_color()].append(piece_at_pos)
        self.board[from_rank - 1][from_file - 1] = None
        self.board[to_rank - 1][to_file - 1] = piece
        piece.update_position(to_rank, to_file)
        self.current_player = constants.COLOR["WHITE"] if self.current_player == constants.COLOR["BLACK"] else constants.COLOR["BLACK"]
        self.halfmoves += 1
        self.update_castling_availability()
        if not simulate: 
            self.update_en_passant_status(alg_from_pos, alg_to_pos)
        self.fen = self.make_fen()
        
        
        if not simulate:
            
            if isinstance(piece, pieces.Pawn):
                if self.try_pawn_promote(alg_to_pos, do_it=False) == constants.PAWN_CAN_PROMOTE:
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
                            moves.append(fen_utils.algebraic_to_coords("g1"))
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
                        moves.append(fen_utils.algebraic_to_coords("c1"))
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
                        moves.append(fen_utils.algebraic_to_coords("g8"))
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
                            moves.append(fen_utils.algebraic_to_coords("c8"))
        return moves
    
    def is_targeted_square(self, coords):
        player = fen_utils.get_opposite_player(self.current_player)
        legal_moves = self.all_legal_moves[player]
        is_targeted = fen_utils.algebraic_to_coords(coords) in legal_moves
        return is_targeted
    
    def castle(self, piece, from_pos, to_pos):
        
        if self.is_king_in_check(self.current_player):
            return False
        
        self.update_castling_availability()
        if not self.castling_availability:
            print("NOT CASTLED")
            
            return False
        
        if to_pos[1] > from_pos[1]:
            castling = 'k' if piece.get_color() == constants.COLOR["BLACK"] else "K"
        elif from_pos[1] > to_pos[1]:
            castling = 'q' if piece.get_color() == constants.COLOR["BLACK"] else 'Q'
            
        if castling not in self.castling_availability:
            print("NOT CASTLED")
            
            return False 
    
        if castling in 'kK':
            r, f = fen_utils.algebraic_to_coords('h8' if castling == 'k' else 'h1')
            r_, f_ = fen_utils.algebraic_to_coords('f8' if castling == 'k' else "f1")
        else:
            r, f = fen_utils.algebraic_to_coords('a8' if castling == 'q' else 'a1')
            r_, f_ = fen_utils.algebraic_to_coords('d8' if castling == 'q' else "d1")
        
        if r and f and r_ and f_:
            rook = self.board[r - 1][f - 1]
            rook.update_position(r_, f_)
            self.board[r_ - 1][f_ - 1] = rook
            self.board[r - 1][f - 1] = None
        
            print("CASTLED!")
            return True
        print("NOT CASTLED")
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
    
    def try_pawn_promote(self, piece_coords, promote_to="queen", do_it=False):
        print("Testing if pawn at ", piece_coords, " can be promoted to ", promote_to)
        rank, file = fen_utils.algebraic_to_coords(piece_coords)
        piece = self.get_piece(piece_coords)
        final_rank = constants.MAX_RANK if piece.get_color() == constants.COLOR["BLACK"] else constants.MIN_RANK 

        can_promote = rank == final_rank
        if not do_it: 
            if can_promote: 
                return constants.PAWN_CAN_PROMOTE
            else: 
                return constants.PAWN_CANNOT_PROMOTE  
       
        if can_promote:
            promoted_piece = self.make_promotion_piece(promote_to, rank, file, piece.get_color())
            self.board[rank - 1][file - 1] = promoted_piece  
            self.fen = self.make_fen()   
            if self.is_game_over():
                print(self.is_checkmate, self.is_stalemate)
                return constants.SUCCESS_PAWN_PROMOTED_CHECKMATE if self.is_checkmate else constants.SUCCESS_PAWN_PROMOTED_STALEMATE
            
            if self.is_king_in_check(self.current_player):
                print("checkl")
                
                return constants.SUCCESS_PAWN_PROMOTED_CHECK
        return constants.SUCCESS_PAWN_PROMOTED
        
    def make_promotion_piece(self, piece_type, rank, file, color):
        if piece_type == "queen":
            return pieces.Queen(rank, file, color)
        
        if piece_type == "rook":
            return pieces.Rook(rank, file, color)

        if piece_type == "knight":
            return pieces.Knight(rank, file, color)
        
        if piece_type == "bishop":
            return pieces.Bishop(rank, file, color)