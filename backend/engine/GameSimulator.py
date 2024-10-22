from engine.board import Board
from engine.Game import Game
from engine.Move import Move

class GameSimulator:
    def __init__(self, log_level=None):
        self.board = Board(log_level=log_level)  
        self.current_game = None
        self.move_generator = None

    def load_game(self, game: Game):
        self.current_game = game
        self.move_generator = self.imitate_gameplay()

    def next_move(self):
        try:
            move_result, move = next(self.move_generator)
            return move_result, move
        except StopIteration:
            return "Game Over", None

    def imitate_gameplay(self):
        for move in self.current_game.moves:
            move_result = self.move_piece(move)
            yield move_result, move

    def move_piece(self, move: Move):
        result = self.board.move_piece(move.from_pos, move.to_pos)
        if move.promotion:
            self.board.current_player = self.board.current_player.opponent()
            self.board.try_pawn_promote(move.to_pos, promote_to=full_name(move.promotion), do_it=True)
            self.board.current_player = self.board.current_player.opponent()
            
            
        return result

    def make_fen(self): 
        return self.board.make_fen()
    
    def get_winner(self):
        return self.board.get_winner()
    
    def show_board(self):
        self.board.print_board(print=True)
        
    def get_stalemate(self):
        return self.board.is_stalemate

def full_name(char):
    promotion_map = {
        'Q': 'queen',
        'R': 'rook',
        'B': 'bishop',
        'N': 'knight',
        'q': 'queen',
        'r': 'rook',
        'b': 'bishop',
        'n': 'knight'
    }

    return promotion_map.get(char, "queen")