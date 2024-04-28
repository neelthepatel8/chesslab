import pytest
from engine import MoveGen
from engine.bitboard.utils import show_raw
from engine.constants import COLOR
from engine.bitboard.bitwise import set_bit, rshift

### LEAPING ATTACKS ###

@pytest.fixture(scope="session", autouse=True)
def init_attack():
    MoveGen.Attack.init()
    yield

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
    

### SLIDING ATTACKTS ###

@pytest.mark.parametrize('rook_position, expected_moves', [
    (0, 0x1010101010101FE),  
    (7, 0x808080808080807F), 
    (56, 0xfe01010101010101), 
    (63, 0x7f80808080808080), 
    (27, 0x8080808f7080808),  
])
def test_movegen_attack_rook_no_blockers(rook_position, expected_moves):
    board = 1 << rook_position
    rook_moves = MoveGen.Attack.rook_move(rook_position, board)
    assert rook_moves == expected_moves


@pytest.mark.parametrize('rook_position, board, expected_moves', [
    (0, 0x10000000011, 0x1010101011e),  
    (7, 0x800084, 0x80807c), 
    (56, 0x8100000000010000,  0xfe01010101010000), 
    (63, 0xa000800000000000, 0x6080800000000000), 
    (27, 0x800002c000008, 0x8080834080808),  
])
def test_movegen_attack_rook_blockers(rook_position, board, expected_moves):
    rook_moves = MoveGen.Attack.rook_move(rook_position, board)
    assert rook_moves == expected_moves

@pytest.mark.parametrize('rook_position, board, expected_moves', [
    (24, 0x10041000000, 0x1017e010101),  
    (3, 0x48, 0x808080808080877), 
    (59, 0x8c00000000000000,  0xf408080808080808), 
    (55, 0x80000000000000, 0x807f808080808080),  
])
def test_movegen_attack_rook_blockers_edge(rook_position, board, expected_moves):
    rook_moves = MoveGen.Attack.rook_move(rook_position, board)
    assert rook_moves == expected_moves

@pytest.mark.parametrize('rook_position, board, expected_moves', [
    (0, 0xffffffffffffffff, 0x102),  
])
def test_movegen_attack_rook_full_board(rook_position, board, expected_moves):
    rook_moves = MoveGen.Attack.rook_move(rook_position, board)
    assert rook_moves == expected_moves

@pytest.mark.parametrize('bishop_position, expected_moves', [
    (0, 0x8040201008040200),  
    (7, 0x102040810204000), 
    (56, 0x2040810204080), 
    (63, 0x40201008040201), 
    (27, 0x8041221400142241),  
])
def test_movegen_attack_bishop_no_blockers(bishop_position, expected_moves):
    board = 1 << bishop_position
    bishop_moves = MoveGen.Attack.bishop_move(bishop_position, board)
    assert bishop_moves == expected_moves


@pytest.mark.parametrize('bishop_position, board, expected_moves', [
    (0, 0x8000001, 0x8040200),  
    (7, 0x40000000080, 0x40810204000), 
    (56, 0x100040000000000,  0x2040000000000), 
    (63, 0x8040000000000000, 0x40000000000000), 
    (27, 0x40000408000240, 0x40201400142240),  
])
def test_movegen_attack_bishop_blockers(bishop_position, board, expected_moves):
    bishop_moves = MoveGen.Attack.bishop_move(bishop_position, board)
    assert bishop_moves == expected_moves

@pytest.mark.parametrize('bishop_position, board, expected_moves', [
    (24, 0x8000001000400, 0x8040200020400),  
    (3, 0x40000008, 0x41221400), 
    (59, 0x814000000000000,  0x14000000000000), 
    (55, 0x80000000000400, 0x4000402010080400),  
])
def test_movegen_attack_bishop_blockers_edge(bishop_position, board, expected_moves):
    bishop_moves = MoveGen.Attack.bishop_move(bishop_position, board)
    assert bishop_moves == expected_moves

@pytest.mark.parametrize('bishop_position, board, expected_moves', [
    (0, 0xffffffffffffffff, 0x200),  
])
def test_movegen_attack_bishop_full_board(bishop_position, board, expected_moves):
    bishop_moves = MoveGen.Attack.bishop_move(bishop_position, board)
    assert bishop_moves == expected_moves











# @pytest.mark.skip()
def test_temp_movegen():
    MoveGen.Attack.init()
    moves = MoveGen.Attack.rook_move(27, 8796395014144)
    show_raw(moves)

