import pytest
from unittest.mock import patch
from engine.board import Board 
from valkyrie.Valkyrie import Valkyrie
from engine.Move import Move

def test_best_move():
    board = Board() 
    valkyrie = Valkyrie()

    moves = [Move("a1", "a3", "p"), Move("b6", "a3", "k"), Move("c8", "d3", "P")]

    with patch('random.choice', return_value=moves[1]):
        assert valkyrie.best_move(board) == moves[1]

def test_best_move_returns_legal_move():
    board = Board()
    valkyrie = Valkyrie()

    moves = [Move("a1", "a3", "p"), Move("b6", "a3", "k"), Move("c8", "d3", "P")]
    board.get_all_legal_moves_with_origin = lambda player: moves

    result = valkyrie.best_move(board)
    assert result in moves
    
@pytest.mark.parametrize("fen, score, expected_white, expected_black", [
    ('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 0, 1042.5, 1042.5),
    ('r1b1k1nr/ppp2ppp/8/3P4/8/2P2N2/PP1P1PqP/RNb1Kn1R w KQkq - 0 1', -16.0, 1024.5, 1040.5),
    ('5R2/8/8/8/8/8/8/3q4 w - - 0 1', -4.75, 5.25, 10.0),
])
def test_evaluate(fen, score, expected_white, expected_black):
    board = Board(fen=fen)
    valkyrie = Valkyrie()
    total_score, white_score, black_score = valkyrie.evaluate(board)
    assert total_score == score
    assert white_score == expected_white
    assert black_score == expected_black
    
