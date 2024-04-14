from engine.Position import Position

class Move():
    def __init__(self, from_pos: Position, to_pos: Position, piece_type: str, promotion=None):
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.piece_type = piece_type
        self.promotion = promotion
    
    def __str__(self):
        return f"{self.piece_type}: {self.from_pos} -> {self.to_pos} {'Promoting!' if self.promotion else ''}"