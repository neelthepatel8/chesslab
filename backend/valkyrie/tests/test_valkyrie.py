import pytest

from unittest.mock import patch
from engine.board import Board 
from valkyrie.Valkyrie import Valkyrie
from engine.Move import Move

@pytest.mark.skip()
def test_best_move():
    board = Board() 
    valkyrie = Valkyrie()

    moves = [Move("a1", "a3", "p"), Move("b6", "a3", "k"), Move("c8", "d3", "P")]

    with patch('random.choice', return_value=moves[1]):
        assert valkyrie.best_move(board) == moves[1]

@pytest.mark.skip()
def test_best_move_returns_legal_move():
    board = Board()
    valkyrie = Valkyrie()

    moves = [Move("a1", "a3", "p"), Move("b6", "a3", "k"), Move("c8", "d3", "P")]
    board.get_all_legal_moves_with_origin = lambda player: moves

    result = valkyrie.best_move(board)
    assert result in moves
    
@pytest.mark.parametrize("fen, score", [
    ('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 0),
    ('r1b1k1nr/ppp2ppp/8/3P4/8/2P2N2/PP1P1PqP/RNb1Kn1R w KQkq - 0 1', -12.5),
    ('5R2/8/8/8/8/8/8/3q4 w - - 0 1', -4.25),
])
def test_evaluate(fen, score):
    board = Board(fen=fen)
    valkyrie = Valkyrie()
    total_score = valkyrie.evaluate(board)
    assert total_score == score

