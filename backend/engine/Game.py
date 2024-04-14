class Game():
    def __init__(self, moves=[], winner=""):
        self.moves = moves 
        self.winner = winner 
        self.name = ""
        
    def set_moves(self, moves):
        self.moves = moves
        
    def set_winner(self, winner):
        self.winner = winner