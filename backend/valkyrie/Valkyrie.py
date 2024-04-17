from engine.board import Board
from engine.Move import Move
import engine.constants as constants
from engine.player.Player import Player
import random

class Valkyrie():
    def __init__(self):
        pass 
    
    def get_all_moves(self, board: Board, player: Player) -> list[Move]:
        return board.get_all_legal_moves_with_origin(player)
        
    def best_move(self, board: Board) -> Move:
        all_legal_moves = self.get_all_moves(board, board.current_player)
        return random.choice(all_legal_moves)
    
    def evaluate(self, board: Board):
        black_score, white_score = 0, 0
        for row in board.board:
            for piece in row:
                if piece is not None:
                    if piece.get_color() == constants.COLOR["BLACK"]:
                        black_score += piece.value
                    
                    else:
                        white_score += piece.value 
            
        score = white_score - black_score
        
        return score, white_score, black_score
        