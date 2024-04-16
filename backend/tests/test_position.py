from engine.Position import Position

def test_position_initialization_with_algebraic():
    pos = Position(algebraic="e2")
    assert pos.rank == 7 and pos.file == 5

def test_position_initialization_with_coords():
    pos = Position(coords=(7, 5))
    assert pos.algebraic == "e2"

def test_position_initialization_with_rank_and_file():
    pos = Position(rank=7, file=5)
    assert pos.algebraic == "e2"

def test_position_initialization_directly():
    pos = Position("e2")
    assert pos.algebraic == "e2"

def test_algebraic_to_coords():
    pos = Position(algebraic="h1")
    assert pos.coords == (8, 8)

def test_coords_to_algebraic():
    pos = Position(coords=(8, 8))
    assert pos.algebraic == "h1"
    
def test_str():
    pos = Position(coords=(8, 8))
    assert pos.__str__() == "h1"
    assert pos.__repr__() == "h1"

def test_is_on_board():
    pos = Position(algebraic="a1")
    assert pos.is_on_board()
    pos = Position(algebraic="i1")
    assert not pos.is_on_board()

def test_position_equality():
    pos1 = Position(algebraic="b2")
    pos2 = Position(algebraic="b2")
    assert pos1 == pos2

def test_position_hash():
    pos_set = set()
    pos1 = Position(algebraic="c3")
    pos2 = Position(algebraic="c3")
    pos_set.add(pos1)
    pos_set.add(pos2)
    assert len(pos_set) == 1

def test_position_comparison():
    pos1 = Position(algebraic="a1")
    pos2 = Position(algebraic="a2")
    assert pos1 > pos2
    assert pos1 >= pos2
    assert pos2 < pos1
    assert pos2 <= pos1

def test_deep_copy():
    pos1 = Position(algebraic="d4")
    pos2 = pos1.deep_copy()
    assert pos1 == pos2 and pos1 is not pos2
