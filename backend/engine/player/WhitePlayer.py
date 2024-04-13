from engine.player.Player import Player
from engine.constants import COLOR

class WhitePlayer(Player):
    def __init__(self):
        super()
        self.color = COLOR["WHITE"]
        
    
    def opponent(self):
        from engine.player.BlackPlayer import BlackPlayer
        return BlackPlayer()
        
    def __str__(self):
        return "WHITE"