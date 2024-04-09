import pytest
from engine.pieces.Rook import Rook
from engine.board import Board
import engine.constants as constants
from engine.fen_utils import algebraic_to_coords, algebraic_list_to_coords
from engine.utils import lists_equal

@pytest.fixture
def empty_board():
    """Fixture for an empty chess board."""
    return Board()

@pytest.fixture
def rook():
    """Fixture for a white rook at the starting position A1."""
    return Rook(1, 1, constants.COLOR["WHITE"])

@pytest.fixture
def rook_at_position():
    """Parameterized fixture for placing a rook at a given position."""
    def _place_rook(rank, file, color):
        return Rook(rank, file, color)
    return _place_rook

@pytest.mark.parametrize("start_pos, end_pos, expected", [
    # Basic movement from start positions Corners
    # White side
    ('a1', 'h1', True),
    ('a1', 'a8', True),
    ('a1', 'a5', True),
    ('a1', 'e1', True), 
    ('h1', 'h8', True),
    ('h1', 'a1', True),
    ('h1', 'h5', True),
    ('h1', 'e1', True),
    
    # Black side
    ('a8', 'h8', True),
    ('a8', 'a1', True),
    ('h8', 'a8', True),
    ('h8', 'h1', True),
    
    # Middle of board
    ('d5', 'd3', True),
    ('d5', 'd7', True),
    ('f4', 'b4', True),
    ('f4', 'h4', True),
    
    # Incorrect movement 
    # Diagonal
    ('a1', 'h8', False),
    ('h1', 'a8', False),
    ('e5', 'b2', False),
    ('e5', 'g3', False),
    
    # Weird Shape movement
    ('c6', 'd4', False),
    ('c6', 'g7', False),
])
def test_rook_movement_legality(start_pos, end_pos, expected, rook_at_position):
    start_rank, start_file = algebraic_to_coords(start_pos)
    end_rank, end_file = algebraic_to_coords(end_pos)
    rook = rook_at_position(start_rank, start_file, constants.COLOR["WHITE"])
    assert rook.can_move((end_rank, end_file)) == expected
    
@pytest.mark.parametrize("start_pos, expected", [
    # Test some basic paths
    ('a1', [['a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8'],
            ['b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']]),
    ('e4', [['f4', 'g4', 'h4'], 
            ['e3', 'e2', 'e1'], 
            ['e5', 'e6', 'e7', 'e8'], 
            ['d4', 'c4', 'b4', 'a4']]),
    ('a6', [['a7', 'a8'], 
            ['a5', 'a4', 'a3', 'a2', 'a1'], 
            ['b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6']]),
])
def test_rook_movement_paths(start_pos, expected, rook_at_position):
    start_rank, start_file = algebraic_to_coords(start_pos)
    rook = rook_at_position(start_rank, start_file, constants.COLOR["WHITE"])
    paths = rook.get_possible_paths() 
    expected = algebraic_list_to_coords(expected)
    assert lists_equal(paths, expected)

    
def test_rook_initial_state(rook):
    assert not rook.has_moved

def test_rook_state_after_move(rook_at_position):
    rook = rook_at_position(1, 4, constants.COLOR["WHITE"])
    rook.update_position(2, 2)
    assert rook.has_moved

