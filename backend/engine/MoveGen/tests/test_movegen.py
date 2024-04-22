import pytest

from engine import MoveGen
from engine.bitboard.utils import show_raw
from engine.constants import COLOR
from engine.bitboard.bitwise import set_bit

@pytest.mark.parametrize("index,  expected_board", [
    (0, 770),
    (2, 3594),  
    (7, 49216),  
    (56, 144959613005987840),
    (63, 4665729213955833856),
    (27, 120596463616),
    (8, 197123),
]) 
def test_movegen_attack_king(index, expected_board):
    attacks = MoveGen.Attack.king()
    assert attacks[index] == expected_board
    

@pytest.mark.parametrize("index,  expected_board", [
    (0, 132096),
    (2, 659712),  
    (7, 4202496),  
    (56, 1128098930098176),
    (63, 9077567998918656),
    (27, 22136263676928),
    (8, 33816580),
]) 
def test_movegen_attack_knight(index, expected_board):
    attacks = MoveGen.Attack.knight()
    assert attacks[index] == expected_board

@pytest.mark.parametrize("index, expected_board", [
    (0, 0),
    (2, 0),  
    (7, 0),  
    (8, 2),
    (56, 562949953421312),
    (63, 18014398509481984),
    (27, 1310720),
])  
def test_movegen_attack_blackpawn(index, expected_board):
    attacks = MoveGen.Attack.pawn(COLOR["BLACK"])
    assert attacks[index] == expected_board
    
@pytest.mark.parametrize("index, expected_board", [
    (0, 512),
    (2, 2560),  
    (7, 16384),  
    (8, 131072),
    (56, 0),
    (63, 0),
    (27, 85899345920),
])  
def test_movegen_attack_whitepawn(index, expected_board):
    attacks = MoveGen.Attack.pawn(COLOR["WHITE"])
    assert attacks[index] == expected_board
    

@pytest.mark.parametrize("index,  expected_board", [
    (0, 132096),
    # (2, 659712),  
    # (7, 4202496),  
    # (56, 1128098930098176),
    # (63, 9077567998918656),
    # (27, 22136263676928),
    # (8, 33816580),
]) 
def test_movegen_attack_bishop(index, expected_board):
    # attacks = MoveGen.Attack.knight()
    # assert attacks[index] == expected_board
    board = 0
    # board = set_bit(board, 25)
    # board = set_bit(board, 11)
    # board = set_bit(board, 30)
    # board = set_bit(board, 35)
    
    board = set_bit(board, 0)
    board = set_bit(board, 13)
    board = set_bit(board, 36)
    board = set_bit(board, 34)
    show_raw(board)
    b = MoveGen.Attack.bishop_at_relative(27, board)
    show_raw(b)

# @pytest.mark.skip()
def test_temp_movegen():
    attacks = MoveGen.Attack.king()
    show_raw(attacks[8])