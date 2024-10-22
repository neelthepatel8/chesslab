from engine.piece import Piece
from engine.constants import COLOR, MAX_RANK
from engine.Position import Position
class Bishop(Piece):
    def __init__(self, position: Position, color: str) -> None:
        super().__init__(position, color)
        self.name = 'b' if color == COLOR['BLACK'] else 'B'
        self.symbol = "♗" if color == COLOR["WHITE"] else "♝"
        self.value = 3.5
        
        self.positional_values = [
            [ -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
            [ -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
            [ -1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
            [ -1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
            [ -1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
            [ -1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
            [ -1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
            [ -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
        ]
        
        self.positional_values = list(reversed(self.positional_values)) if color == COLOR["BLACK"] else self.positional_values
        
        
    def can_move(self, to_pos: Position):
        if not super().can_move(to_pos):
            return False
        
        to_rank, to_file = to_pos.rank, to_pos.file

        rank_difference = abs(self.position.rank - to_rank)
        file_difference = abs(self.position.file - to_file)

        return rank_difference == file_difference

    def get_possible_paths(self):
        paths = []
        directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]

        for d_rank, d_file in directions:
            path = []
            for step in range(1, MAX_RANK):
                new_rank = self.position.rank + step * d_rank
                new_file = self.position.file + step * d_file
                new_position = Position(rank=new_rank, file=new_file)
                if new_position.is_on_board():
                    path.append(new_position)
                else:
                    break
            if path:
                paths.append(path)

        return paths