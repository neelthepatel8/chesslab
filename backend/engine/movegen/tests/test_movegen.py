import pytest


import engine.movegen.movegen as MoveGen
from engine.bitboard.utils import bitmask_to_positions, show

@pytest.mark.parametrize("func, index,  expected_positions", [
    (MoveGen.rook, 0, set([1, 2, 3, 4, 5, 6, 7, 8, 16, 24, 32, 40, 48, 56])),
    (MoveGen.rook, 8, set([0, 16, 24, 32, 40, 48, 56, 9, 10, 11, 12, 13, 14, 15])),  
    (MoveGen.rook, 27, set([19, 11, 3, 35, 43, 51, 59, 26, 25, 24, 28, 29, 30, 31])),  
    (MoveGen.rook, 63, set([62, 61, 60, 59, 58, 57, 56, 55, 47, 39, 31, 23, 15, 7])),
    (MoveGen.knight, 0, set([10, 17])),
    (MoveGen.knight, 8, set([2, 18, 25])),
    (MoveGen.knight, 27, set([10, 12, 17, 21, 33, 37, 42, 44])),
    (MoveGen.knight, 63, set([46, 53])),
])
def test_movegen(func, index, expected_positions):
    moves = func()
    positions = set(bitmask_to_positions(moves[index]))
    assert positions == expected_positions

@pytest.mark.parametrize("func, index, expected_bitboard", [
    (MoveGen.queen, 0, 9313761861428380670),
    (MoveGen.queen, 18, 9530782384287059477),
])
def test_movegen_ray(func, index, expected_bitboard):
    moves = func()
    print(f'{show(moves[index])}')
    assert moves[index] == expected_bitboard