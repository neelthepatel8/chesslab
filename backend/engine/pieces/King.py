from engine.piece import Piece
from engine.constants import COLOR
from engine.Position import Position

class King(Piece):
    def __init__(self, position: Position, color: str) -> None:
        super().__init__(position, color)
        self.name = 'k' if color == COLOR['BLACK'] else 'K'
        self.symbol = "♔" if color == COLOR["WHITE"] else "♚"
        self.value = 1000.0
        
        self.positional_values = [
            [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [ -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
            [ -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
            [  2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0 ],
            [  2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0 ]
        ]
        
        self.positional_values = list(reversed(self.positional_values)) if color == COLOR["BLACK"] else self.positional_values


    def can_move(self, to_pos: Position):
        
        if not super().can_move(to_pos):
            return False
        
        to_rank, to_file = to_pos.rank, to_pos.file

        rank_difference = abs(self.position.rank - to_rank)
        file_difference = abs(self.position.file - to_file)

        return (rank_difference <= 1) and (file_difference <= 1)

    def get_possible_paths(self):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]
        paths = []

        for d_rank, d_file in directions:
            new_rank = self.position.rank + d_rank
            new_file = self.position.file + d_file
            new_position = Position(rank=new_rank, file=new_file)
            if new_position.is_on_board():
                paths.append([new_position])
        return paths
