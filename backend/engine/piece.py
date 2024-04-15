from engine.constants import MAX_RANK, MAX_FILE, MIN_RANK, MIN_FILE
from engine.Position import Position
class Piece():
    def __init__(self, position: Position, color: str) -> None:

        self.position = position
        self.color = color
        self.has_moved = False

    def can_move(self, to_pos: Position):

        if self.position == to_pos: 
            return False

        to_rank, to_file = to_pos.rank, to_pos.file

        rank_check = MIN_RANK <= to_rank <= MAX_RANK
        file_check = MIN_FILE <= to_file <= MAX_FILE

        return rank_check and file_check

    def can_kill(self, to_pos: Position) -> bool:
        return self.can_move(to_pos)

    def get_possible_moves(self):

        possible_moves = []

        for to_rank in range(1, MAX_RANK + 1):
            for to_file in range(1, MAX_FILE + 1):
                to_position = Position(rank=to_rank, file=to_file)
                if self.can_move(to_position):
                    possible_moves.append(to_position)

        return possible_moves
    
    def get_name(self):
        return self.name

    def get_color(self):
        return self.color
    
    def update_position(self, position):
        self.position = position
        self.has_moved = True
        
    def get_algebraic_pos(self):
        return self.position.algebraic
    
    def check_bounds(self, value: int):
        return MIN_RANK <= value <= MAX_RANK
    
    def deep_copy(self):
        position_copy = self.position.deep_copy() if self.position else None
        piece_copy = type(self)(position_copy, self.color)
        piece_copy.has_moved = self.has_moved  
        piece_copy.name = self.name  
        return piece_copy