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
    assert board.current_player == BlackPlayer()
    assert board.halfmoves == 0
    assert board.fullmoves == 0
    assert lists_equal(board.castling_availability, ['k', 'K', 'q', 'Q'])
    assert board.dead_pieces == {'black': [], 'white': []}
    assert not board.is_stalemate
    assert not board.is_checkmate
    assert board.king_in_check is None
    assert board.winner is None
    assert board.en_passant.target_square is None 

@pytest.mark.parametrize("fen, expected_player, expected_moves", [
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", WhitePlayer(), 0),
    ("rnbqkbnr/pppppppp/8/8/3Q4/8/PPPPPPPP/RNBQKBNR b kq - 1 10", BlackPlayer(), 1),
])
def test_board_initialization_custom_fen(fen, expected_player, expected_moves):
    board = Board(fen=fen)
    assert board.fen == fen
    assert board.current_player == expected_player
    assert board.halfmoves == expected_moves
    assert boards_equal(board.board, fen_utils.build_board_from_fen(fen))