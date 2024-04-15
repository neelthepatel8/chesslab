import pytest
from engine.player.BlackPlayer import BlackPlayer
from engine.player.WhitePlayer import WhitePlayer
from engine.player.Player import Player
from engine.constants import COLOR

@pytest.mark.parametrize("player, expected_color, expected_str", [
    (BlackPlayer(), COLOR["BLACK"], "BLACK"),
    (WhitePlayer(), COLOR["WHITE"], "WHITE"),
    (Player(), None, "none"),
])
def test_player_color_and_str(player, expected_color, expected_str):
    assert player.color == expected_color
    assert str(player) == expected_str

def test_opponent_functionality():
    black_player = BlackPlayer()
    white_player = WhitePlayer()
    player = Player()
    assert isinstance(black_player.opponent(), WhitePlayer)
    assert isinstance(white_player.opponent(), BlackPlayer)
    assert isinstance(player.opponent(), Player)

def test_player_equality():
    player1 = BlackPlayer()
    player2 = BlackPlayer()
    player3 = WhitePlayer()
    assert player1 == player2
    assert player1 != player3
