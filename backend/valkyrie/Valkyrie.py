from engine.board import Board
from engine.Move import Move
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