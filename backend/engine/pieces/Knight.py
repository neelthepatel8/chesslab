from engine.piece import Piece
from engine.constants import COLOR
from engine.Position import Position

class Knight(Piece):
    def __init__(self, position: Position, color: str) -> None:
        super().__init__(position, color)
        self.name = 'n' if color == COLOR['BLACK'] else 'N'
        self.symbol = "♘" if color == COLOR["WHITE"] else "♞"
        self.value = 3.5
        
        self.positional_values = [
                [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
                [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
                [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
                [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
                [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
                [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
                [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
                [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
            ]
        
        

    def can_move(self, to_pos: Position):
        move_offsets = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        paths = set()

        for d_rank, d_file in move_offsets:
            new_rank = self.position.rank + d_rank
            new_file = self.position.file + d_file
            new_position = Position(rank=new_rank, file=new_file)
            if new_position.is_on_board():
                paths.add(new_position)

        return to_pos in paths

    def get_possible_paths(self):
        move_offsets = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        paths = []

        for d_rank, d_file in move_offsets:
            new_rank = self.position.rank + d_rank
            new_file = self.position.file + d_file
            new_position = Position(rank=new_rank, file=new_file)
            if new_position.is_on_board():
                paths.append([new_position])
        return paths