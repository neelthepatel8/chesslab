import pytest
from engine.pieces.Bishop import Bishop
from engine.board import Board
import engine.constants as constants
from engine.fen_utils import algebraic_list_to_positions
from engine.utils import lists_equal
from engine.Position import Position

@pytest.fixture
def empty_board():
    """Fixture for an empty chess board."""
    return Board()

@pytest.fixture
def bishop():
    """Fixture for a white bishop at the starting position A1."""
    return Bishop(Position(rank=1, file=1), constants.COLOR["WHITE"])

@pytest.fixture
def bishop_at_position():
    """Parameterized fixture for placing a bishop at a given position."""
    def _place_bishop(position,  color):
        return Bishop(Position(algebraic=position), color)
    return _place_bishop

@pytest.mark.parametrize("start_pos, end_pos, expected", [
    # Basic movement from start positions Corners
    # White side
    ('a1', 'h8', True),
    ('h1', 'a8', True),
    
    # Black side
    ('a8', 'h1', True),
    ('h8', 'a1', True),
    
    # Middle of board
    ('e5', 'h8', True),
    ('e5', 'a1', True),
    ('e5', 'h2', True),
    ('e5', 'b8', True),
    
    # Incorrect movement 
    # Horizontal
    ('a1', 'h1', False),
    ('a1', 'a8', False),
    ('d5', 'h5', False),
    ('d5', 'd1', False),
    ('d5', 'd8', False),
    ('d5', 'a5', False),
    
    # Weird Shape movement
    ('c6', 'd4', False),
])
def test_bishop_movement_legality(start_pos, end_pos, expected, bishop_at_position):
    bishop = bishop_at_position(start_pos, constants.COLOR["WHITE"])
    assert bishop.can_move(Position(algebraic=end_pos)) == expected
    
@pytest.mark.parametrize("start_pos, expected", [
    # Test some basic paths
    ('a1', [['b2', 'c3', 'd4', 'e5', 'f6', 'g7', 'h8']]),
    ('e4', [['f3', 'g2', 'h1'], 
            ['f5', 'g6', 'h7'], 
            ['d5', 'c6', 'b7', 'a8'], 
            ['d3', 'c2', 'b1']]),
])
def test_bishop_movement_paths(start_pos, expected, bishop_at_position):
    bishop = bishop_at_position(start_pos, constants.COLOR["WHITE"])
    paths = bishop.get_possible_paths()
    expected = algebraic_list_to_positions(expected)
    assert lists_equal(paths, expected)

    
def test_bishop_initial_state(bishop):
    assert not bishop.has_moved

def test_bishop_state_after_move(bishop_at_position: Bishop):
    bishop = bishop_at_position(Position(rank=1, file=4), constants.COLOR["WHITE"])
    bishop.update_position(Position(rank=2, file=2))
    assert bishop.has_moved

