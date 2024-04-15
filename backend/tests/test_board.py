import pytest
from engine.board import Board
import engine.constants as constants
from engine.Position import Position
from engine.GameSimulator import GameSimulator
from engine.player.BlackPlayer import BlackPlayer
from engine.player.WhitePlayer import WhitePlayer
from engine.PGNParser import PGNParser
from engine.utils import boards_equal, lists_equal
import engine.fen_utils as fen_utils

@pytest.fixture
def empty_board():
    """Fixture for an empty chess board."""
    return Board()

@pytest.mark.skip("Temporarily not testing since takes a long time, PLEASE COMMENT SKIP BEFORE DEPLOYING")
@pytest.mark.parametrize("file_name", [
    ('twic1535'),
])
def test_board_checkmate_full_games(file_name):
    parser = PGNParser(file_name=file_name, multi=True)
    games = parser.parse(checkmate=True)
    
    for index, game in enumerate(games):

        simulator = GameSimulator()
        simulator.load_game(game)
        winner = game.winner

        winner = None if winner == "1/2-1/2" else BlackPlayer() if winner == "0-1" else WhitePlayer()
        if index == 0:
            print(f"\nSimulating game {index}: ", game.name, end=", ")
        else: 
            print(f"Simulating game {index}: ", game.name, end=", ")
            
        while True:
            result, move = simulator.next_move()
            if result == "Game Over":
                break
            
            # print(move)
            # if winner is not None: 
            #     simulator.show_board()

        print(f"Simulation over. Played {len(simulator.current_game.moves)} moves, winner is: ", simulator.get_winner(), " expected: ", winner)
        assert type(simulator.get_winner()) == type(winner)
        

def test_board_initialization_default():
    board = Board()
    assert board.fen == constants.START_FEN
    assert board.board is not None
    assert board.current_player == WhitePlayer()
    assert board.halfmoves == 0
    assert board.fullmoves == 1
    assert board.castling_availability == set(['k', 'K', 'q', 'Q'])
    assert board.dead_pieces == {'black': [], 'white': []}
    assert not board.is_stalemate
    assert not board.is_checkmate
    assert board.king_in_check is None
    assert board.winner is None
    assert board.en_passant.target_pawn_position is None 

@pytest.mark.parametrize("fen, expected_player, expected_moves", [
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", WhitePlayer(), 0),
    ("rnbqkbnr/pppppppp/8/8/3Q4/8/PPPPPPPP/RNBQKBNR b kq - 1 10", BlackPlayer(), 1),
])
def test_board_initialization_custom_fen(fen, expected_player, expected_moves):
    board = Board(fen=fen)
    assert board.fen == fen
    assert board.current_player == expected_player
    assert board.halfmoves == expected_moves
    assert boards_equal(board.board, fen_utils.build_board_from_fen(fen), verbose=True)
    
@pytest.mark.parametrize("fen, expected_available, expected_eligible, expected_target, expected_color", [
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", False, None, None, None),
    ("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1", True, Position(algebraic="e3"), Position(algebraic="e4"), constants.COLOR["WHITE"]),
])    
def test_board_initialization_en_passant(fen, expected_available, expected_eligible, expected_target, expected_color):
    board = Board(fen=fen)
    assert board.en_passant.available == expected_available
    assert board.en_passant.eligible_square == expected_eligible
    assert board.en_passant.target_pawn_position == expected_target
    assert board.en_passant.pawn_color == expected_color
    
@pytest.mark.parametrize("fen, expected_castling", [
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", {'K', 'Q', 'k', 'q'}),
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b Kq - 0 1", {'K', 'q'}),
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1", set())
])
def test_castling_availability(fen, expected_castling):
    board = Board(fen=fen)
    assert board.castling_availability == expected_castling


@pytest.mark.parametrize("fen, expected_halfmoves, expected_fullmoves", [
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 0, 1),
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b Kq - 10 5", 10, 5)
])
def test_move_counters(fen, expected_halfmoves, expected_fullmoves):
    board = Board(fen=fen)
    assert board.halfmoves == expected_halfmoves
    assert board.fullmoves == expected_fullmoves

    
@pytest.mark.parametrize("fen", [
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"),
    ("rnbqkbnr/pppppppp/8/8/3Q4/8/PPPPPPPP/RNBQKBNR b kq - 1 10"),
    ("rn1q1rk1/1b3ppp/ppPb1n2/3p4/8/2N1PNP1/PB1P1PBP/R2Q1RK1 b - - 0 12"),
])
def test_make_fen_with_init(fen):
    board = Board(fen=fen)
    board.fen = ""
    assert board.make_fen() == fen

@pytest.mark.parametrize("fen, move, expected", [
    (
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 
        ("g1", "f3"), 
        "rnbqkbnr/pppppppp/8/8/8/5N2/PPPPPPPP/RNBQKB1R w KQkq - 0 1"
    ),
    (
        "rn1q1rk1/1b3ppp/ppPb1n2/3p4/8/2N1PNP1/PB1P1PBP/R2Q1RK1 b - - 0 12", 
        ("f6", "e4"), 
        "rn1q1rk1/1b3ppp/ppPb4/3p4/4n3/2N1PNP1/PB1P1PBP/R2Q1RK1 b - - 0 12"
    ),
])
def test_make_fen_after_move(fen, move, expected):
    board = Board(fen=fen)
    from_pos, to_pos = move
    from_pos = Position(algebraic=from_pos)
    to_pos = Position(algebraic=to_pos)
    
    board.move(from_pos, to_pos)
    
    assert board.make_fen() == expected

@pytest.mark.parametrize("fen, availability, eligible_square, expected", [
    (
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 
        False,
        None,
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    ),
    (
        "rn1q1rk1/1b3ppp/ppPb1n2/3p4/8/2N1PNP1/PB1P1PBP/R2Q1RK1 b - - 0 12", 
        True,
        Position(algebraic="h3"), 
        "rn1q1rk1/1b3ppp/ppPb1n2/3p4/8/2N1PNP1/PB1P1PBP/R2Q1RK1 b - h3 0 12"
    ),
])
def test_make_fen_with_en_passant(fen, availability, eligible_square, expected):
    board = Board(fen=fen)
    board.en_passant.available = availability
    board.en_passant.eligible_square = eligible_square
    assert board.make_fen() == expected
    
    
@pytest.mark.parametrize("fen, castling, expected", [
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1", {'K', "k"}, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w Kk - 0 1"),
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1", {'K', "q"}, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w Kq - 0 1"),
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1", {'q', "Q"}, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w Qq - 0 1"),
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", {'k'}, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w k - 0 1"),
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", {'q'}, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w q - 0 1"),
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", set(), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1"),
])
def test_make_fen_with_castling(fen, castling, expected):
    board = Board(fen=fen)
    board.castling_availability = castling
    assert board.make_fen() == expected
    
    
@pytest.mark.parametrize("fen, player, expected", [
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1", BlackPlayer(), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b - - 0 1"),
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1", WhitePlayer(), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1"),
])
def test_make_fen_with_player(fen, player, expected):
    board = Board(fen=fen)
    board.current_player = player
    assert board.make_fen() == expected
    
    


