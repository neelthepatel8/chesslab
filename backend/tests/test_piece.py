from engine.constants import MAX_RANK, MAX_FILE
from engine.Position import Position
from engine.piece import Piece

def test_piece_initialization():
    pos = Position(rank=1, file=1)
    piece = Piece(pos, "white")
    assert piece.position == pos and piece.color == "white"

def test_can_move():
    pos = Position(rank=1, file=1)
    to_pos = Position(rank=1, file=2)
    piece = Piece(pos, "white")
    assert piece.can_move(to_pos)
    assert not piece.can_move(pos)

def test_can_kill():
    pos = Position(rank=1, file=1)
    to_pos = Position(rank=1, file=2)
    piece = Piece(pos, "white")
    assert piece.can_kill(to_pos)

def test_get_possible_moves():
    pos = Position(rank=2, file=2)
    piece = Piece(pos, "white")
    possible_moves = piece.get_possible_moves()
    assert len(possible_moves) == (MAX_RANK * MAX_FILE - 1)

def test_get_name():
    pos = Position(rank=1, file=1)
    piece = Piece(pos, "white")
    piece.name = "Knight"
    assert piece.get_name() == "Knight"

def test_get_color():
    pos = Position(rank=1, file=1)
    piece = Piece(pos, "black")
    assert piece.get_color() == "black"

def test_update_position():
    pos = Position(rank=1, file=1)
    new_pos = Position(rank=1, file=2)
    piece = Piece(pos, "white")
    piece.update_position(new_pos)
    assert piece.position == new_pos and piece.has_moved is True

def test_get_algebraic_pos():
    pos = Position(rank=1, file=1)
    piece = Piece(pos, "white")
    assert piece.get_algebraic_pos() == "a8"

def test_check_bounds():
    pos = Position(rank=1, file=1)
    piece = Piece(pos, "white")
    assert piece.check_bounds(1) and not piece.check_bounds(0)

def test_deep_copy():
    pos = Position(rank=1, file=1)
    piece = Piece(pos, "white")
    piece_copy = piece.deep_copy()
    assert piece_copy == piece and piece_copy is not piece

def test_piece_equality():
    pos1 = Position(rank=1, file=1)
    pos2 = Position(rank=1, file=1)
    piece1 = Piece(pos1, "white")
    piece2 = Piece(pos2, "white")
    assert piece1 == piece2
