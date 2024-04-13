from engine.player.Player import Player
from engine.player.WhitePlayer import WhitePlayer

class BlackPlayer(Player):
    def __init__(self):
        super()
        
    def opponent(self):
        return WhitePlayer()
    
    def __str__(self):
        return "BLACK"
        