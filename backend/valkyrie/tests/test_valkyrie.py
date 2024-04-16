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
