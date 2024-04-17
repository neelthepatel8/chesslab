from engine.Position import Position

class Move():
    def __init__(self, from_pos: Position, to_pos: Position, piece_type: str, promotion=None):
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.piece_type = piece_type
        self.promotion = promotion
    
    def __repr__(self):
        return f"{self.piece_type}: {self.from_pos} -> {self.to_pos} {'Promoting!' if self.promotion else ''}"
    
    def __eq__(self, other):
        return type(self) == type(other) and self.from_pos == other.from_pos and self.to_pos == other.to_pos and self.piece_type == other.piece_type

    
    def __hash__(self) -> int:
        return hash(self.from_pos) ^ hash(self.to_pos) ^ hash(self.piece_type)