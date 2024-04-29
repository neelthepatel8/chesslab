from engine.board import Board
from engine.Move import Move
import engine.constants as constants
from engine.player.Player import Player
from engine.piece import Piece
from engine import MoveGen
from graphviz import Digraph



class Valkyrie():
    def __init__(self):
        self.king_move_cache = MoveGen.Attack.king()
        self.knight_move_cache = MoveGen.Attack.knight()
        self.whitepawn_move_cache = MoveGen.Attack.pawn(constants.COLOR["BLACK"])
        self.blackpawn_move_cache = MoveGen.Attack.pawn(constants.COLOR["WHITE"])
    
    def get_all_moves(self, board: Board, player: Player) -> list[Move]:
        return board.get_all_legal_moves_with_origin(player)
        
    def evaluate(self, board: Board):
        black_score, white_score = 0, 0
        for row in board.board:
            for piece in row:
                if piece is not None:
                    piece_value = self.get_piece_value(piece)
                    if piece.get_color() == constants.COLOR["BLACK"]:
                        black_score += piece_value
                    else:
                        white_score += piece_value
            
        score = white_score - black_score
        
        return score
    
    def get_piece_value(self, piece: Piece) -> int:
        return piece.value + self.get_positional_value(piece)
    
    def get_positional_value(self, piece: Piece) -> int:
        position = piece.position
        rank, file = position.coords
        position_value = piece.positional_values[rank - 1][file - 1]
        return position_value
    
    def best_move(self, board: Board):                                
        dot = Digraph(format='png') 

        player = board.current_player
        moves = self.get_all_moves(board, player)

        initial_board_copy = board.deep_copy()
        current_score = self.evaluate(initial_board_copy)
        best_score, best_move = current_score, None

        root_id = str(initial_board_copy) 
        initial_board_state = initial_board_copy.print_board()
        dot.node(root_id, label=f'Initial Score: {current_score}\n{initial_board_state}')

        for move in moves:
            board_copy = board.deep_copy()
            board_copy.move(move.from_pos, move.to_pos)
            new_score = self.evaluate(board_copy)
            
            is_better_move = new_score >= best_score if player == constants.COLOR["WHITE"] else new_score <= best_score
            if is_better_move:
                best_score = new_score
                best_move = move
            
            # Update graph:
            move_id = str(board_copy)  
            board_state = board_copy.print_board()
            dot.node(move_id, label=f'Move: {move}\nScore: {new_score}\n{board_state}')
            dot.edge(root_id, move_id, label=str(move))

        dot.render('output/move_tree', view=False) 
        return best_move
