from __future__ import annotations
import engine.constants as constants
import engine.fen_utils as fen_utils
from engine.piece import Piece
import engine.pieces as pieces
import copy
from engine.enpassant.EnPassantStatus import EnPassantStatus

from engine.Position import Position

from engine.player.Player import Player   
from engine.logging import get_logger
from engine.player.WhitePlayer import WhitePlayer
from engine.player.BlackPlayer import BlackPlayer



class Board():
    def __init__(self, fen=constants.START_FEN, log_level=None) -> None:
        super().__init__()
        
        self.logger = get_logger(log_level)
        self.log(f"Initializing Board with FEN: {fen}")
            
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
        
        self.winner = None
        
        self.all_legal_moves = {
            constants.COLOR["BLACK"]: [],
            constants.COLOR["WHITE"]: []
        }
        
        available, eligible_square, target_pawn, pawn_color = fen_utils.get_en_passant_status(fen)
        self.en_passant = EnPassantStatus(
            available=available,
            eligible_square=eligible_square,
            target_pawn_position=target_pawn,
            pawn_color=pawn_color,
        )
        
        self.log(f"Board initialized with FEN: {fen}")
        self.log(f"Initial board state:\n{self.print_board()}")

    def log(self, message):
        if self.logger is not None:
            self.logger.debug(message)

    def make_fen(self):
        self.log("Starting FEN generation")
            
        active = "w" if isinstance(self.current_player, WhitePlayer) else "b"
        en_passant = self.en_passant.eligible_square.algebraic if self.en_passant.available else '-'
        standard_castling_order = 'KQkq'
        castling = ''.join(sorted((c for c in self.castling_availability if c in standard_castling_order), 
                            key=lambda x: standard_castling_order.index(x))) if self.castling_availability else '-'

        if not castling: 
            castling = "-"

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

        self.log(f"FEN generated: {self.fen}")

        self.log(f"Current board state after FEN generation:\n{self.print_board()}")

        return self.fen

    def get_piece(self, position: Position) -> Piece | None:
        rank, file = position.rank, position.file
        piece = self.board[rank - 1][file - 1]
        self.log(f"Getting piece at position: {position}")
        self.log(f"Piece retrieved: {piece}")
        return piece

    def set_piece(self, position: Position, piece: Piece):
        rank, file = position.rank, position.file
        self.log(f"Setting piece at position {position} to {piece}")
        self.log(f"Piece set at position {position}")
        self.log(f"Board state:\n{self.print_board()}")
        self.board[rank - 1][file - 1] = piece

    def clear_square(self, position: Position):
        self.log(f"Clearing square at position {position}")
        self.log("Square cleared")
        self.log(f"Board state:\n{self.print_board()}")
        self.set_piece(position, None)

    def get_pseudo_legal_moves(self, position: Position, log=False) -> list:
        self.log(f"Generating pseudo-legal moves for position {position}")
            
        if self.is_stalemate or self.is_checkmate: 
            self.log("No moves available due to stalemate or checkmate")
            return []
        
        piece = self.get_piece(position)
        if not piece:
            self.log("No piece at the given position; returning empty move list")
            return []

        all_paths = piece.get_possible_paths()
        valid_moves = []
        
        for path in all_paths:
            
            valid_path = []
            
            for pos in path:
                if not pos.is_on_board():
                    self.log(f"Position {pos} is not on the board")
                    break

                piece_at_pos = self.get_piece(pos)

                if piece_at_pos:
                    if piece_at_pos.get_color() != piece.get_color():
                        if piece.can_kill(pos):
                            valid_path.append(pos)
                    break
                        
                else:
                    if not self.king_in_check:
                        valid_moves.extend(self.get_castlable_moves(piece))
                    
                    if piece.can_move(pos):
                        valid_path.append(pos)
                    
                    if isinstance(piece, pieces.Pawn):
                        
                        if self.en_passant.available and self.en_passant.pawn_color != piece.get_color():
                            possible = self.check_en_passant_possible_for_piece(piece)               
                                             
                            if possible:
                                valid_moves.append(self.en_passant.eligible_square)

            valid_moves.extend(valid_path)
        
        unique_moves = list(set(valid_moves))
        self.log(f"Generated pseudo legal moves for {position}: {unique_moves}")

        return unique_moves


    def get_all_pseudo_legal_moves(self, player: Player) -> list:
        self.log(f"Generating all pseudo-legal moves for player {player.color}")

        moves = []
        for row in self.board:
            for piece in row:
                if not piece: 
                    continue 
                if piece.get_color() != player.color: 
                    continue
                moves.extend(self.get_pseudo_legal_moves(piece.position))
        
        self.log(f"All generated moves for {player.color}: {moves}")
        
        return moves
    
    def deep_copy_board(self):
        copy_board = Board()
        copy_board.board = [[None for _ in range(constants.MAX_FILE)] for _ in range(constants.MAX_RANK)]
        for r in range(constants.MAX_RANK):
            for c in range(constants.MAX_FILE):
                if self.board[r][c] is not None:
                    copy_board.board[r][c] = self.board[r][c].deep_copy()
        return copy_board
    
    def deep_copy(self) -> Board:
        copy_board = self.deep_copy_board()
        copy_board.fen = self.fen
        copy_board.current_player = self.current_player
        copy_board.halfmoves = self.halfmoves
        copy_board.fullmoves = self.fullmoves
        copy_board.castling_availability = copy.deepcopy(self.castling_availability)
        copy_board.dead_pieces = copy.deepcopy(self.dead_pieces)
        return copy_board

    def is_move_legal(self, from_pos: Position, to_pos: Position) -> bool:
        self.log(f"Checking if move: {from_pos} -> {to_pos} is legal..")
        board_copy = self.deep_copy()
        piece = board_copy.get_piece(from_pos)
        color = piece.get_color() 
        if color:
            player_to_check = BlackPlayer() if color == constants.COLOR["BLACK"] else WhitePlayer()
        else:
            player_to_check = board_copy.current_player.opponent()
        board_copy.simulate_move(from_pos, to_pos)
        self.log(f"Board state after simulated move:\n{board_copy.print_board()}")
        self.log(f"Checking if king is in check for {player_to_check} from is move legal")
        if board_copy.is_king_in_check(player_to_check):
            self.log("King is in check, illegal move.")
            return False

        self.log("King is not in check, legal move.")
        return True

    def simulate_move(self, from_pos: Position, to_pos: Position):
        self.log(f"Simulating move from {from_pos} to {to_pos}")
        self.move_piece(from_pos, to_pos, simulate=True)
        
    def get_legal_moves(self, position: Position, log=False) -> list:
        legal_moves = []
        self.log(f"Getting pseudo legal moves from get legal moves for {position}")
        pseudo_legal_moves = self.get_pseudo_legal_moves(position, log)
        for to_pos in pseudo_legal_moves:
            if self.is_move_legal(position, to_pos):
                legal_moves.append(to_pos)
        
        legal_moves = list(set(legal_moves))
        self.log(f"Legal moves for position {position}: {legal_moves}")
        return legal_moves
    
    def get_all_legal_moves(self, player: Player, log=False) -> list:
        self.log(f"Getting all legal moves for player: {player}")
        moves = []
        for row in self.board:
            for piece in row:
                if not piece: 
                    continue 
                if piece.get_color() != player.color: 
                    continue
                moves.extend(self.get_legal_moves(piece.position, log))
        self.all_legal_moves[player.color] = moves
        
        moves = list(set(moves))
        self.log(f"All legal moves for {player.color}: {moves}")
        return moves


    def is_king_in_check(self, player: Player) -> bool:
        king = self.get_king_location(player)
        self.log(f"Checking if king in check for player: {player} whose king is at {king}")
        opponent = player.opponent()
        all_possible_moves = self.get_all_pseudo_legal_moves(opponent)
        self.log(f"For that got all pseudo legal moves for {opponent} and current player is {player}: {all_possible_moves}")
        for move in all_possible_moves:
            if move == king:
                self.king_in_check = player
                return True

        self.king_in_check = None
        return False

    def get_king_location(self, player: Player) -> Position:
        for row in self.board:
            for piece in row:
                if not piece: 
                    continue 
                if piece.get_color() != player.color: 
                    continue 
                if piece.get_name().lower() == 'k':
                    self.log(f"King found for {player} at {piece.position}")
                    return piece.position
        self.log("King not found for player")
        return Position()
    
    def update_en_passant_status(self, from_pos: Position, to_pos: Position):
        from_rank, _ = from_pos.rank, from_pos.file 
        to_rank, to_file = to_pos.rank, to_pos.file
        self.log("Updating en passant status")
        
        moved_piece = self.get_piece(to_pos)
        
        if isinstance(moved_piece, pieces.Pawn) and abs(to_rank - from_rank) == 2:
            eligible_square_rank = to_rank  + 1 if moved_piece.get_color() == constants.COLOR["WHITE"] else to_rank - 1
            eligible_square = Position(rank=eligible_square_rank, file=to_file)
            self.en_passant.set(eligible_square, to_pos, moved_piece.get_color())
            self.log(f"En passant set for {moved_piece.get_color()} at {eligible_square}")

        else:
            self.en_passant.clear()
            self.log("En passant status cleared")
            

    def check_en_passant_possible_for_piece(self, piece: Piece):
        self.log(f"Checking en passant possibility for piece at {piece.position}")
        
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
        self.log(f"Received command for move: {from_pos} -> {to_pos}")
        piece = self.get_piece(from_pos)
        piece_at_pos = self.get_piece(to_pos)

        if not piece: 
            self.log("No piece at source position to move")
            return constants.ERROR_NO_PIECE_TO_MOVE
        
        if not simulate and not self.is_valid_move(from_pos, to_pos):
            self.log("Move not valid")
            return constants.ERROR_MOVE_NOT_POSSIBLE

        kill_status = constants.NO_KILL
        special_status = constants.NO_CHECK
        
        if not piece_at_pos:
            has_castled = self.check_for_castle(from_pos, to_pos)
            has_en_passant = self.check_for_en_passant(from_pos, to_pos)
                            
            if has_castled:
                special_status = constants.CASTLED

            if has_en_passant:
                kill_status = constants.KILL
            
        kill_status = self.move(from_pos, to_pos)
        self.update_board(from_pos, to_pos)
        
        # if not simulate: print(f"Doing post move checks for move {from_pos} -> {to_pos}")
        special_status = self.post_move_checks(from_pos, to_pos) if not simulate else constants.NO_CHECK
        self.current_player = self.current_player.opponent() if not simulate else self.current_player
        self.log(f"Swapped current player from {self.current_player.opponent()} -> {self.current_player}")
        
        self.fen = self.make_fen()
        
        self.log(f"Completed move: {from_pos} -> {to_pos} with kill status: {kill_status} and special status: {special_status}")
        self.log(f"Updated FEN: {self.fen}")
        return kill_status, special_status
        
    def update_board(self, from_pos: Position, to_pos: Position):
        self.log("Updating board state post-move")
        
        if self.get_piece(to_pos) and self.get_piece(to_pos).get_color() == constants.COLOR["BLACK"]:
            self.fullmoves += 1
        
        self.halfmoves += 1
        self.update_castling_availability()
        self.update_en_passant_status(from_pos, to_pos)

        
    def post_move_checks(self, from_pos: Position, to_pos: Position):
        self.log(f"Checking post-move conditions for {from_pos} -> {to_pos}")
         
        if self.try_pawn_promote(to_pos, do_it=False) == constants.PAWN_CAN_PROMOTE:
            self.log("Pawn promotion possible after move")
            return constants.PROMOTE_POSSIBLE

        self.log(f"Checking if game is over for {self.current_player.opponent()}")
        if self.is_game_over():
            self.log("Game over")
            return constants.CHECKMATE if self.is_checkmate else constants.STALEMATE
        
        if self.is_king_in_check(self.current_player.opponent()): 
            self.log("Check condition detected")
            return constants.CHECK
        
        return constants.NO_CHECK
        
    def is_valid_move(self, from_pos: Position, to_pos: Position):
        self.log(f"Validating move {from_pos} -> {to_pos}")
        possible_moves = self.get_pseudo_legal_moves(from_pos)
        if to_pos not in possible_moves:
            self.log("Move not valid based on pseudo-legal moves")
            return False 
        return True
    
    def move(self, from_pos: Position, to_pos: Position):
        self.log(f"Executing move {from_pos} -> {to_pos}")
        
        piece = self.get_piece(from_pos)
        self.clear_square(from_pos)
        killed_piece = self.get_piece(to_pos)
        self.set_piece(to_pos, piece)
        piece.update_position(to_pos)
        if killed_piece: 
            self.log(f"Piece killed at {to_pos}")
            self.dead_pieces[killed_piece.get_color()].append(killed_piece)
            return constants.KILL
        
        self.log("No kill occurred during the move")
        return constants.NO_KILL

        
    def check_for_castle(self, from_pos: Position, to_pos: Position):
        self.log(f"Checking for castle move: {from_pos} to {to_pos}")
        
        piece = self.get_piece(from_pos)
        has_castled = False
        if isinstance(piece, pieces.King) and abs(to_pos.file - from_pos.file) > 1:
            has_castled = self.castle(piece, from_pos, to_pos)
            
        if has_castled:
            self.log("Castle move performed successfully")
        else:
            self.log("Castle move not possible")

        return has_castled  
    
    def check_for_en_passant(self, from_pos: Position, to_pos: Position):
        piece = self.get_piece(from_pos)
        
        if isinstance(piece, pieces.Pawn) and self.en_passant.available:
            if self.check_en_passant_possible_for_piece(piece):
                if to_pos == self.en_passant.eligible_square:
                    removed_pawn = self.get_piece(self.en_passant.target_pawn_position)
                    self.clear_square(self.en_passant.target_pawn_position)
                    self.dead_pieces[removed_pawn.get_color()].append(removed_pawn)
                    self.log(f"En passant executed, removing pawn at {self.en_passant.target_pawn_position}")
                    return True
        self.log("En passant not executed")
        return False
              
    def get_castlable_moves(self, piece):
        self.log(f"Getting castlable moves for king at {piece.position}")
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
        player = self.current_player.opponent()
        legal_moves = self.all_legal_moves[player.color]
        self.log(f"Checking if square {position} is targeted by {player}: {position in legal_moves}")
        return position in legal_moves
    
    def castle(self, piece: Piece, from_pos: Position, to_pos: Position):
        
        if self.is_king_in_check(self.current_player):
            return False
        
        self.update_castling_availability()
        if not self.castling_availability:
            return False
        
        if to_pos.file > from_pos.file:
            castling = 'k' if piece.get_color() == constants.COLOR["BLACK"] else "K"
        elif from_pos.file > to_pos.file:
            castling = 'q' if piece.get_color() == constants.COLOR["BLACK"] else 'Q'
            
        if castling not in self.castling_availability:
            
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

        if pos1.is_on_board() and pos2.is_on_board():
            rook = self.get_piece(pos1)
            self.set_piece(pos2, rook)
            self.clear_square(pos1)
            rook.update_position(pos2)
            return True
        return False 
    
    def update_castling_availability(self):
        self.log("Updating castling availability based on board state")
        
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

        self.log(f"Updated castling availability: {self.castling_availability}")

    def is_game_over(self):
        self.log("Checking if the game is over")
        
        if self.is_stalemate or self.is_checkmate:
            return True
        
        current = self.current_player # White
        opponent = self.current_player.opponent()
        all_legal_moves = self.get_all_legal_moves(opponent, log=False)
        self.log(f"All legal moves for player {opponent} are: {all_legal_moves}")
        
        if len(all_legal_moves) == 0:
            if self.are_only_kings_on_board():
                self.is_stalemate = True
                self.winner = None
                self.log("Game is a stalemate due to only kings left on the board")
            
            else:
                self.log(f"No legal moves possible for player {opponent}, checking for check conditions")
                king_in_check = self.is_king_in_check(opponent)
                if king_in_check:
                    self.is_checkmate = True
                    self.winner = current
                    self.log("Game over with a checkmate")
                    
                else:
                    self.is_stalemate = True
                    self.winner = None
                    self.log("Game over with a stalemate due to no legal moves")

                    
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
        rank, _ = position.rank, position.file
        piece = self.get_piece(position)
        
        if not isinstance(piece, pieces.Pawn):
            self.log(f"No pawn at position {position} to promote")
            return constants.PAWN_CANNOT_PROMOTE
        
        final_rank = constants.MAX_RANK if piece.get_color() == constants.COLOR["BLACK"] else constants.MIN_RANK 

        can_promote = rank == final_rank
        if not do_it: 
            if can_promote: 
                self.log(f"Pawn at {position} can be promoted")
                
                return constants.PAWN_CAN_PROMOTE
            else: 
                self.log(f"Pawn at {position} cannot be promoted yet")
                return constants.PAWN_CANNOT_PROMOTE  
       
        if can_promote:
            promoted_piece = self.make_promotion_piece(promote_to, position, piece.get_color())
            self.set_piece(position, promoted_piece)
            self.fen = self.make_fen() 
            self.log(f"Pawn at {position} promoted to {promote_to}")
              
            if self.is_game_over():
                self.log("Game over after promotion")
                
                return constants.SUCCESS_PAWN_PROMOTED_CHECKMATE if self.is_checkmate else constants.SUCCESS_PAWN_PROMOTED_STALEMATE
            
            if self.is_king_in_check(self.current_player):
                self.log(f"King in check after promotion at {position}")
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

        
    def get_winner(self):
        return self.winner
    
    def print_board(self, print=False):
        board_string = ""
        for row in self.board:
            for piece in row:
                if piece is None:
                    board_string += '. '
                else:
                    board_string += f"{piece.symbol} "
            board_string += '\n'

        if self.king_in_check is not None:
            board_string += f"King in check: {self.king_in_check}\n"
        if print: 
            print(board_string)

        return board_string
    
    
