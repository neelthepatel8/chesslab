import pytest
from engine.pieces.King import King
from engine.board import Board
import engine.constants as constants
from engine.fen_utils import algebraic_to_coords, algebraic_list_to_coords
from engine.utils import lists_equal

@pytest.fixture
def empty_board():
    """Fixture for an empty chess board."""
    return Board()

@pytest.fixture
def king_at_position():
    """Parameterized fixture for placing a king at a given position."""
    def _place_king(rank, file, color):
        return King(rank, file, color)
    return _place_king

@pytest.mark.parametrize("start_pos, end_pos, expected", [
    # Basic movements
    ('e1', 'e2', True), 
    ('e1', 'd2', True),  
    ('e1', 'd1', True),  
    ('e1', 'f1', True),  
    ('e1', 'e8', False), 
    ('e1', 'a5', False),
])
def test_king_movement_legality(start_pos, end_pos, expected, king_at_position):
    start_rank, start_file = algebraic_to_coords(start_pos)
    end_rank, end_file = algebraic_to_coords(end_pos)
    king = king_at_position(start_rank, start_file, constants.COLOR["WHITE"])
    assert king.can_move((end_rank, end_file)) == expected

@pytest.mark.parametrize("start_pos, expected", [
    ('e1', [['d1'], ['d2'], ['e2'], ['f2'], ['f1']]),
    ('e8', [['d8'], ['d7'], ['e7'], ['f7'], ['f8']]),
])
def test_king_movement_paths(start_pos, expected, king_at_position):
    start_rank, start_file = algebraic_to_coords(start_pos)
    king = king_at_position(start_rank, start_file, constants.COLOR["WHITE"])
    paths = king.get_possible_paths() 
    expected = algebraic_list_to_coords(expected)
    assert lists_equal(paths, expected, verbose=True)

def test_king_initial_state(king_at_position):
    king = king_at_position(1, 5, constants.COLOR["WHITE"]) 
    assert not king.has_moved

def test_king_state_after_move(king_at_position):
    king = king_at_position(1, 5, constants.COLOR["WHITE"])
    king.update_position(2, 5) 
    assert king.has_moved
