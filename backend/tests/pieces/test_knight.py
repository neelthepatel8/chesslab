import pytest
from engine.pieces.Knight import Knight
from engine.board import Board
import engine.constants as constants
from engine.Position import Position

@pytest.fixture
def empty_board():
    """Fixture for an empty chess board."""
    return Board()

@pytest.fixture
def knight_at_position():
    """Parameterized fixture for placing a knight at a given position."""
    def _place_knight(position, color):
        return Knight(Position(algebraic=position), color)
    return _place_knight

@pytest.mark.parametrize("start_pos, end_pos, expected", [
    # Valid movements
    ('b1', 'c3', True), 
    ('b1', 'a3', True), 
    ('b1', 'd2', True), 
    ('e4', 'd6', True), 
    ('e4', 'f6', True), 
    ('e4', 'g3', True),

    # Invalid movements
    ('b1', 'b2', False), 
    ('b1', 'c2', False),
    ('e4', 'e5', False), 
    ('e4', 'f5', False),
])
def test_knight_movement_legality(start_pos, end_pos, expected, knight_at_position):
    knight = knight_at_position(start_pos, constants.COLOR["WHITE"])
    assert knight.can_move(Position(algebraic=end_pos)) == expected

def test_knight_initial_state(knight_at_position):
    knight = knight_at_position(Position(rank=1, file=2), constants.COLOR["WHITE"]) 
    assert not knight.has_moved

def test_knight_state_after_move(knight_at_position):
    knight = knight_at_position(Position(rank=1, file=2), constants.COLOR["WHITE"])  
    knight.update_position(Position(rank=3, file=3)) 
    assert knight.has_moved
