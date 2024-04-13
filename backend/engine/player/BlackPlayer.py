from engine.player.Player import Player
from engine.constants import COLOR
class BlackPlayer(Player):
    def __init__(self):
        super()
        self.color = COLOR["BLACK"]
        
    def opponent(self):
        from engine.player.WhitePlayer import WhitePlayer
        return WhitePlayer()
    
    def __str__(self):
        return "BLACK"
        