import pytest
from engine.pieces.Pawn import Pawn
from engine.board import Board
import engine.constants as constants
from engine.fen_utils import algebraic_to_coords, algebraic_list_to_coords
from engine.utils import lists_equal


@pytest.fixture
def empty_board():
    """Fixture for an empty chess board."""
    return Board()

@pytest.fixture
def pawn_at_position():
    """Parameterized fixture for placing a pawn at a given position."""
    def _place_pawn(rank, file, color):
        return Pawn(rank, file, color)
    return _place_pawn

# WHITE PAWN
@pytest.mark.parametrize("start_pos, end_pos, expected", [
    # Single Valid Moves:
        # From start position
        ('c2', 'c3', True), 
        ('a2', 'a3', True), 

        # From other places on board
        ('d4', 'd5', True),
        ('f7', 'f8', True),

    # Single Invalid Moves:
        # Backwards movement
        ('c2', 'c1', False),
        ('d4', 'd3', False),

        # Sideways movement
        ('c2', 'd2', False),
        ('c2', 'b2', False),
        ('d4', 'c4', False),
        ('d4', 'e4', False),

        # Diagonal movement
        ('c2', 'd3', False),
        ('c2', 'b3', False),
        ('c2', 'd1', False),
        ('c2', 'b1', False),
        ('d4', 'e5', False),
        ('d4', 'c5', False),
        ('d4', 'e3', False),
        ('d4', 'c3', False),

    # Double Valid moves:
        ('c2', 'c4', True),
        ('a2', 'a4', True),
    
    # Double Invalid moves:
        # Sideways movement
        ('c2', 'e2', False),
        ('c2', 'a2', False),

        # Not at starting position
        ('c3', 'c5', False),
        ('e5', 'e7', False),
    
    # Multiple squares movement:
        ('c2', 'f8', False),
        ('c2', 'c7', False),
])
def test_white_pawn_movement_legality(start_pos, end_pos, expected, pawn_at_position):
    start_rank, start_file = algebraic_to_coords(start_pos)
    pawn = pawn_at_position(start_rank, start_file, constants.COLOR["WHITE"])
    assert pawn.can_move(end_pos) == expected


# BLACK PAWN
@pytest.mark.parametrize("start_pos, end_pos, expected", [
    # Single Valid Moves:
        # From start position
        ('c7', 'c6', True), 
        ('a7', 'a6', True), 

        # From other places on board
        ('d4', 'd3', True),
        ('f2', 'f1', True),

    # Single Invalid Moves:
        # Backwards movement
        ('c7', 'c8', False),
        ('d4', 'd5', False),

        # Sideways movement
        ('c7', 'd7', False),
        ('c7', 'b7', False),
        ('d4', 'c4', False),
        ('d4', 'e4', False),

        # Diagonal movement
        ('c7', 'd6', False),
        ('c7', 'b6', False),
        ('c7', 'd8', False),
        ('c7', 'b8', False),
        ('d4', 'e5', False),
        ('d4', 'c5', False),
        ('d4', 'e3', False),
        ('d4', 'c3', False),

    # Double Valid moves:
        ('c7', 'c5', True),
        ('a7', 'a5', True),
    
    # Double Invalid moves:
        # Sideways movement
        ('c7', 'e7', False),
        ('c7', 'a7', False),

        # Not at starting position
        ('c6', 'c4', False),
        ('d4', 'd2', False),
    
    # Multiple squares movement:
        ('c7', 'f3', False),
        ('c7', 'c2', False),
])
def test_black_pawn_movement_legality(start_pos, end_pos, expected, pawn_at_position):
    start_rank, start_file = algebraic_to_coords(start_pos)
    end_rank, end_file = algebraic_to_coords(end_pos)
    pawn = pawn_at_position(start_rank, start_file, constants.COLOR["BLACK"])
    assert pawn.can_move((end_rank, end_file)) == expected

@pytest.mark.parametrize("start_pos, expected", [
    # Starting position 
    ('c2', [['c3'], ['c3', 'c4']]),

    # Non-starting position 
    ('c4', [['c5']]),

    # End of board
    ('c8', []),
])
def test_pawn_movement_paths(start_pos, expected, pawn_at_position):
    start_rank, start_file = algebraic_to_coords(start_pos)
    pawn = pawn_at_position(start_rank, start_file, constants.COLOR["WHITE"])
    paths = pawn.get_possible_paths() 
    expected = algebraic_list_to_coords(expected)
    assert lists_equal(paths, expected, verbose=True)

def test_pawn_initial_state(pawn_at_position):
    pawn = pawn_at_position(1, 2, constants.COLOR["WHITE"]) 
    assert not pawn.has_moved

def test_pawn_state_after_move(pawn_at_position):
    pawn = pawn_at_position(1, 2, constants.COLOR["WHITE"])  
    pawn.update_position(3, 3) 
    assert pawn.has_moved


# WHITE PAWN KILL
@pytest.mark.parametrize("start_pos, end_pos, expected", [
    # Valid Kills
        # From start position
        ('c2', 'd3', True), 
        ('c2', 'b3', True), 
        ('a2', 'b3', True), 
        ('h2', 'g3', True), 

        # From other places on board
        ('d4', 'e5', True),
        ('d4', 'c5', True),

    # Invalid Kills
        # Straight kill
        ('c2', 'c3', False),
        ('c2', 'c4', False),

        # Sideways Kill
        ('c2', 'e2', False),
        ('c2', 'a2', False),

    # Multiple squares Kill:
        ('c2', 'f8', False),
        ('c2', 'c7', False),
])
def test_pawn_capture(start_pos, end_pos, expected, pawn_at_position):
    start_rank, start_file = algebraic_to_coords(start_pos)
    end_rank, end_file = algebraic_to_coords(end_pos)
    pawn = pawn_at_position(start_rank, start_file, constants.COLOR["WHITE"])
    assert pawn.can_kill((end_rank, end_file)) == expected


# BLACK PAWN KILL
@pytest.mark.parametrize("start_pos, end_pos, expected", [
    # Valid Kills
        # From start position
        ('c7', 'd6', True), 
        ('c7', 'b6', True), 
        ('a7', 'b6', True), 
        ('h7', 'g6', True), 

        # From other places on board
        ('d4', 'e3', True),
        ('d4', 'c3', True),

    # Invalid Kills
        # Straight kill
        ('c7', 'c6', False),
        ('c2', 'c5', False),

        # Sideways Kill
        ('c2', 'e2', False),
        ('c2', 'a2', False),

    # Multiple squares Kill:
        ('c7', 'f8', False),
        ('c7', 'c1', False),
])
def test_pawn_capture(start_pos, end_pos, expected, pawn_at_position):
    start_rank, start_file = algebraic_to_coords(start_pos)
    end_rank, end_file = algebraic_to_coords(end_pos)
    pawn = pawn_at_position(start_rank, start_file, constants.COLOR["BLACK"])
    assert pawn.can_kill((end_rank, end_file)) == expected