import pytest
from engine.board import Board
import engine.constants as constants
from engine.Position import Position
from engine.GameSimulator import GameSimulator
from engine.player.BlackPlayer import BlackPlayer
from engine.player.WhitePlayer import WhitePlayer
from engine.PGNParser import PGNParser
from engine.utils import boards_equal
import engine.fen_utils as fen_utils
import engine.pieces as pieces
from dotenv import load_dotenv
import os


@pytest.fixture
def empty_board():
    """Fixture for an empty chess board."""
    return Board()

# @pytest.mark.skip("Temporarily not testing since takes a long time, PLEASE COMMENT SKIP BEFORE DEPLOYING")
@pytest.mark.parametrize("file_name", [
    ('twic1535'),
])
def test_board_checkmate_full_games(file_name):
    parser = PGNParser(file_name=file_name, multi=True)
    games = parser.parse(checkmate=True)

    
    for index, game in enumerate(games):

        
        # Set to 'DEBUG' for log file generation.
        log_level = None
        simulator = GameSimulator(log_level=log_level)
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
        print(f"Game Name: {game.name}")
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
    print(board.make_fen(), fen)
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
    

@pytest.mark.parametrize("fen, position,  expected", [
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", Position(algebraic="d2"), pieces.Pawn),
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1", Position(algebraic="h8"), pieces.Rook),
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1", Position(algebraic="d4"), None),
])
def test_get_piece(fen, position, expected):
    board = Board(fen=fen)
    if expected is None:
        assert board.get_piece(position) == expected
        return
        
    assert type(board.get_piece(position)) == expected
    
    
@pytest.mark.parametrize("fen, position, piece", [
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",Position(algebraic="d5"), pieces.Pawn),
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", Position(algebraic="a2"),  pieces.King),
])
def test_set_piece(fen, position, piece):
    board = Board(fen=fen)
    piece = piece(position, constants.COLOR["WHITE"])
    board.set_piece(position, piece)
    assert board.get_piece(position) == piece

@pytest.mark.parametrize("fen, position", [
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", Position(algebraic="b2")),
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", Position(algebraic="e8")),
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", Position(algebraic="e4")),
])
def test_clear_square(fen, position):
    board = Board(fen=fen)
    board.clear_square(position)
    assert board.get_piece(position) is None
    
    
def test_deep_copy_basic_attributes():
    board = Board()
    board.fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board.current_player = WhitePlayer()
    board.halfmoves = 10
    board.fullmoves = 5
    board.castling_availability = {'K', 'Q'}
    board.dead_pieces = [pieces.Pawn(Position(), constants.COLOR["WHITE"])]

    copied_board = board.deep_copy()

    assert copied_board.fen == board.fen
    assert copied_board.current_player == board.current_player
    assert copied_board.halfmoves == board.halfmoves
    assert copied_board.fullmoves == board.fullmoves
    assert copied_board.castling_availability == board.castling_availability
    assert copied_board.dead_pieces == board.dead_pieces

def test_deep_copy_mutable_objects():
    board = Board()
    board.castling_availability = {'K', 'Q'}
    board.dead_pieces = [pieces.Pawn(Position(), constants.COLOR["WHITE"])]

    copied_board = board.deep_copy()

    # Modify the original and check copied values
    board.castling_availability.add('k')
    board.dead_pieces.append(pieces.Knight(Position(), constants.COLOR["WHITE"]))

    assert copied_board.castling_availability == {'K', 'Q'} 
    assert len(copied_board.dead_pieces) == 1  
    assert type(copied_board.dead_pieces[0]) == pieces.Pawn

def test_reference_integrity():
    board = Board()
    board.castling_availability = {'K', 'Q'}
    board.dead_pieces = [pieces.Pawn(Position(), constants.COLOR["WHITE"])]

    copied_board = board.deep_copy()

    copied_board.castling_availability.add('k')
    copied_board.dead_pieces.append(pieces.Knight(Position(), constants.COLOR["WHITE"]))

    assert 'k' not in board.castling_availability
    assert len(board.dead_pieces) == 1
    assert type(board.dead_pieces[0]) == pieces.Pawn

@pytest.mark.parametrize("setup_fen, from_pos, to_pos, expected", [
    # Move put the king in check
    ("8/8/8/3q4/8/8/3K4/8 w - - 0 1", Position("d2"), Position("d3"), False),
    
    # Move takes the king out of check
    ("8/8/8/3q4/3k4/8/8/8 b - - 0 1", Position("d4"), Position("d5"), True),
    
    # Neutral move the king is not in check
    ("8/8/8/8/8/2N5/3K4/8 w - - 0 1", Position("c3"), Position("b5"), True),
    
    # Capture removes check
    ("8/8/8/3q4/3k4/8/8/8 b - - 0 1", Position("d4"), Position("d5"), True),
])
def test_is_move_legal(setup_fen, from_pos, to_pos, expected):
    board = Board(fen=setup_fen, log_level="DEBUG")
    assert board.is_move_legal(from_pos, to_pos) == expected

@pytest.mark.parametrize("setup_fen, position, expected_moves", [
    # A simple scenario where a knight has two legal moves
    ("8/8/8/2n5/8/8/8/8 b - - 0 1", Position("c5"), [Position("d7"), Position("e6"), Position("d3"), Position("e4"), Position("b7"), Position("a6"), Position("a4"), Position("b3")]),
    
    # King in check, must move
    ("8/8/8/8/8/8/3Q1k2/8 b - - 0 1", Position("f2"), [Position("f1"), Position("g1"), Position("f3"), Position("g3")]),
    
    # King has no legal moves due to check
    ("8/8/8/8/8/8/5Q2/7k b - - 0 1", Position("h1"), []),
    
    # Testing en passant move legality
    ("8/ppp2ppK/8/8/3Pp3/P7/1PP1PP1k/8 b - d3 0 1", Position("e4"), [Position("d3"), Position("e3")]), 
    
    # Castling scenario, checking if castling moves are legal when not in check
    ("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1", Position("e1"), [Position("c1"), Position("g1"), Position("d1"), Position("f1"), Position("d2"), Position("e2"), Position("f2")]),
])
def test_get_legal_moves(setup_fen, position, expected_moves):
    board = Board(fen=setup_fen)
    legal_moves = board.get_legal_moves(position)
    assert set(legal_moves) == set(expected_moves)

@pytest.mark.parametrize("setup_fen, player, expected", [
    # Initial scenario already provided
    ("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1", BlackPlayer(), False),
    # Simple direct check by a rook
    ("8/8/8/8/8/8/2R3k1/7K b - - 0 1", BlackPlayer(), True),
    # Knight check
    ("8/8/8/3n4/8/8/6k1/7K b - - 0 1", BlackPlayer(), True),
    # Pawn check
    ("8/8/8/8/8/1P6/6k1/7K b - - 0 1", BlackPlayer(), True),
    # Multiple attackers
    ("8/8/2q5/4r3/8/8/6k1/7K b - - 0 1", BlackPlayer(), True),
    # Edge of the board, no check
    ("8/8/8/8/8/8/6k1/7R b - - 0 1", BlackPlayer(), False),
    # Edge of the board, with check
    ("8/8/8/8/8/8/8/R6k b - - 0 1", BlackPlayer(), True)
])
def test_king_in_check(setup_fen, player, expected):
    board = Board(fen=setup_fen)
    assert board.is_king_in_check(player) == expected

@pytest.mark.parametrize("setup_fen, winner", [
    ("8/8/8/8/8/8/8/R6k b - - 0 1", BlackPlayer()),
    ("8/8/8/8/8/8/8/R6k b - - 0 1", WhitePlayer()),
    ("8/8/8/8/8/8/8/R6k b - - 0 1", None),
])
def test_winner(setup_fen, winner):
    board = Board(fen=setup_fen)
    board.winner = winner
    assert board.get_winner() == winner


def test_get_all_legal_moves():
    board = Board()
    player = WhitePlayer()
    moves = board.get_all_legal_moves(player)
    assert isinstance(moves, list)
    assert len(moves) > 0

def test_post_move_checks():
    board = Board()
    board.post_move_checks(Position("e2"), Position("e4"))

def test_check_for_en_passant():
    board = Board()
    board.set_piece(Position("e5"), pieces.Pawn(Position("e5"), constants.COLOR["BLACK"]))
    board.en_passant.set(Position("e6"), Position("e5"), "black")
    result = board.check_for_en_passant(Position("e5"), Position("e6"))
    assert not result

def test_is_game_over():
    board = Board()
    assert not board.is_game_over()

def test_are_only_kings_on_board():
    board = Board()
    board.board = [[None for _ in range(8)] for _ in range(8)]
    board.set_piece(Position("e1"), pieces.King(Position("e1"), constants.COLOR["WHITE"]))
    board.set_piece(Position("e1"), pieces.King(Position("e8"), constants.COLOR["BLACK"]))
    assert board.are_only_kings_on_board()

def test_make_promotion_piece():
    board = Board()
    new_queen = board.make_promotion_piece("queen", Position("e8"), "white")
    assert isinstance(new_queen, pieces.Queen)
    
    new_knight = board.make_promotion_piece("knight", Position("e8"), constants.COLOR["WHITE"])
    assert isinstance(new_knight, pieces.Knight)

