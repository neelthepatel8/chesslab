from engine.FastBoard.FastBoard import FastBoard
from engine.player import Player, BlackPlayer, WhitePlayer
import engine.MoveGen as MoveGen 
from engine.constants import COLOR
from engine.Position import Position
from engine.Move import Move


def get_all_moves(board: FastBoard, player: Player):
    
    moves = []
    
    for index in range(64):
        position = Position(index=index)
        piece = board.get_piece(position)
        
        piece_type = piece.get_name()
        
        if piece is None or piece.get_color() != player:
            continue

        attacks = None 
        
        if piece_type in 'kK':
            # Search king cache
            pass 
        elif piece_type in 'nN':
            # Search Knightr cache
            pass 
        elif piece_type in 'pP':
            # Search pawn cache 
            pass 
        
        elif piece_type in 'BRQbrq':
            # Get attacks using magic bitboard. 
            pass 
            
        else: 
            raise NameError("Piece Type not recognized")
        
         