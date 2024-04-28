from engine.Position import Position
from engine.constants import START_FEN
import engine.pieces as pieces
from engine.constants import COLOR
from engine.bitmanipulation.utils import count_bits, lsb
from engine.FastBoard.FastBoard import FastBoard
from engine.Move import Move

import pytest 

def test_position_to_index():
    board = FastBoard()

    index = 0
    for r in range(8):
        for f in range(8):
            position = Position(lsrcoords=(r, f))
            assert board.position_to_index(position) == index
            
            index += 1

@pytest.mark.parametrize('fen, expected_board', [ 
    ('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', '1111111111111111000000000000000000000000000000001111111111111111'),   
    ('7k/8/8/8/8/8/8/K1Q5 w - - 0 1', '1010000000000000000000000000000000000000000000000000000000000001'),   
                         
])
def test_fastboard(fen, expected_board):
    board = FastBoard(fen=fen)
    actual_board = board.board()
    assert f"{actual_board:064b}" == expected_board

@pytest.mark.parametrize('position, expected_type, expected_color', [ 
    ("a2", pieces.Pawn, COLOR["WHITE"]),   
])
def test_get_piece(position, expected_type, expected_color):
    board = FastBoard(START_FEN)
    piece = board.get_piece(Position(algebraic=position))
    assert type(piece) == expected_type
    assert piece.color == expected_color


@pytest.mark.parametrize("board, expected_count", [
    (36187135283560448, 5),
    (36187135283568660, 8),
])
def test_bit_counter(board, expected_count):
    assert count_bits(board) == expected_count
    
@pytest.mark.parametrize("board, expected", [
    (1125899906842624, 50),
    (1125900443713536, 29),
    (128, 7),
    (18446744073709551615, 0),
    (0, -1),
])
def test_lsb(board, expected):
    assert lsb(board) == expected


def test_fastboard_move_piece():
    print('startrd')
    move = Move(Position("b3"), Position("d3"), "p", color=COLOR["BLACK"])
    board = FastBoard(fen="4K3/8/8/8/8/1p6/8/4k3 w - - 0 1")
    print(board.bitboards)
    board.show()
    board.move_piece(move)
    board.show()

# @pytest.mark.skip("Temporary test to visualize board, not needed")
# def test_temp_show():
#     bitboard = BitBoard(START_FEN)
#     print(f"{bitboard.bitboards[8][1]:064b}")
