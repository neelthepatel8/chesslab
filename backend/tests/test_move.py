from engine.Move import Move
from engine.Position import Position

def test_move_init():
    move = Move(from_pos=Position("h1"), to_pos=Position("h2"), piece_type="p")
    assert move.from_pos == Position("h1")
    assert move.to_pos == Position("h2")
    
def test_move_str():
    move = Move(from_pos=Position("h1"), to_pos=Position("h2"), piece_type="pawn")
    assert str(move) == "pawn: h1 -> h2 "
