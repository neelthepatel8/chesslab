from engine.player.Player import Player
from engine.player.BlackPlayer import BlackPlayer

class WhitePlayer(Player):
    def __init__(self):
        super()
    
    def opponent(self):
        return BlackPlayer()
        
    def __str__(self):
        return "WHITE"