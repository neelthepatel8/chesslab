from engine.Game import Game
from engine.Move import Move
from engine.Position import Position

def test_game_init():
    game = Game()
    assert game.moves == []
    assert game.winner == ""
    
def test_game_set_moves():
    game = Game()
    moves=[Move(Position(0, 0), Position(0,1), "p")]
    game.set_moves(moves)
    assert game.moves == moves
    
def test_game_set_winner():
    game = Game()
    game.set_winner("black")
    assert game.winner == "black"
