import pytest
from engine.board import Board
import engine.constants as constants
from engine.Position import Position
from engine.GameSimulator import GameSimulator
from engine.player.BlackPlayer import BlackPlayer
from engine.player.WhitePlayer import WhitePlayer
from engine.PGNParser import PGNParser

@pytest.fixture
def empty_board():
    """Fixture for an empty chess board."""
    return Board()

@pytest.mark.parametrize("file_name, expected", [
    ('twic1535', constants.COLOR["WHITE"]),
   
])
def test_board_different_full_games(file_name, expected):
    parser = PGNParser(file_name=file_name, multi=True)
    games = parser.parse()
    
    for index, game in enumerate(games):

        simulator = GameSimulator()
        simulator.load_game(game)
        winner = game.winner

        winner = None if winner == "1/2-1/2" else BlackPlayer() if winner == "0-1" else WhitePlayer()
        print(f"Starting game {index}: ", game.name)

        while True:
            result, move = simulator.next_move()
            if result == "Game Over":
                break
            
            # print(move)
            # if winner is not None: 
            #     simulator.show_board()

        print(f"Game over. Played {len(simulator.current_game.moves)} moves, winner is: ", simulator.get_winner(), " expected: ", winner)
        assert type(simulator.get_winner()) == type(winner)
 

