from engine.board import Board
from engine.Game import Game
from engine.Position import Position

class GameSimulator:
    def __init__(self):
        self.board = Board()  
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
            print("All moves have been played.")
            return "Game Over", None

    def imitate_gameplay(self):
        for move in self.current_game.moves:
            move_result = self.move_piece(move.from_pos, move.to_pos)
            print(f"Moved from {move.from_pos} to {move.to_pos}")
            yield move_result, move

    def move_piece(self, from_pos: Position, to_pos: Position):
        return self.board.move_piece(from_pos, to_pos)

    def make_fen(self): 
        return self.board.make_fen()
