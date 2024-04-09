import pytest
from engine.pieces.Queen import Queen
from engine.board import Board
import engine.constants as constants
from engine.fen_utils import algebraic_to_coords, algebraic_list_to_coords
from engine.utils import lists_equal

@pytest.fixture
def empty_board():
    """Fixture for an empty chess board."""
    return Board()

@pytest.fixture
def queen_at_position():
    """Parameterized fixture for placing a queen at a given position."""
    def _place_queen(rank, file, color):
        return Queen(rank, file, color)
    return _place_queen

@pytest.mark.parametrize("start_pos, end_pos, expected", [
    # Diagonal movements
    ('d4', 'h8', True),
    ('d4', 'a7', True),
    ('d4', 'a1', True),
    ('d4', 'g1', True),
    
    # Straight line movements
    ('d4', 'd8', True),
    ('d4', 'd1', True),
    ('d4', 'a4', True),
    ('d4', 'h4', True),
    
    # Invalid movements
    ('d4', 'c6', False),
    ('d4', 'e6', False),
])
def test_queen_movement_legality(start_pos, end_pos, expected, queen_at_position):
    start_rank, start_file = algebraic_to_coords(start_pos)
    end_rank, end_file = algebraic_to_coords(end_pos)
    queen = queen_at_position(start_rank, start_file, constants.COLOR["WHITE"])
    assert queen.can_move((end_rank, end_file)) == expected

@pytest.mark.parametrize("start_pos, expected", [
    ('d4', [['e4', 'f4', 'g4', 'h4'], 
            ['d5', 'd6', 'd7', 'd8'],
            ['c4', 'b4', 'a4'],
            ['d3', 'd2', 'd1'],
            ['e5', 'f6', 'g7', 'h8'],
            ['c5', 'b6', 'a7'],
            ['e3', 'f2', 'g1'],
            ['c3', 'b2', 'a1']]),
])
def test_queen_movement_paths(start_pos, expected, queen_at_position):
    start_rank, start_file = algebraic_to_coords(start_pos)
    queen = queen_at_position(start_rank, start_file, constants.COLOR["WHITE"])
    paths = queen.get_possible_paths() 
    expected = algebraic_list_to_coords(expected)
    assert lists_equal(paths, expected)

def test_queen_initial_state(queen_at_position):
    queen = queen_at_position(1, 4, constants.COLOR["WHITE"])
    assert not queen.has_moved

def test_queen_state_after_move(queen_at_position):
    queen = queen_at_position(1, 4, constants.COLOR["WHITE"])
    queen.update_position(2, 2)
    assert queen.has_moved
