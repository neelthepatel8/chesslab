from engine.Position import Position
class EnPassantStatus:
    def __init__(self, available=False, eligible_square=None, target_pawn_position=None, pawn_color=None):
        self.available = available 
        self.eligible_square = eligible_square
        self.target_pawn_position = target_pawn_position
        self.pawn_color = pawn_color

    def set(self, eligible_square: Position, target_pawn_position: Position, pawn_color: str):
        self.available = True
        self.eligible_square = eligible_square
        self.target_pawn_position = target_pawn_position
        self.pawn_color = pawn_color

    def clear(self):
        self.available = False
        self.eligible_square = None
        self.target_pawn_position = None
        self.pawn_color = None