from engine.piece import Piece
from engine.constants import COLOR, MAX_RANK, MAX_FILE


class Knight(Piece):
    def __init__(self, rank, file, color) -> None:
        super().__init__(rank, file, color)
        self.name = 'n' if color == COLOR['BLACK'] else 'N'


    def get_possible_paths(self):
        move_offsets = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        paths = []

        for d_rank, d_file in move_offsets:
            new_rank = self.rank + d_rank
            new_file = self.file + d_file
            if 1 <= new_rank <= MAX_RANK and 1 <= new_file <= MAX_FILE:
                paths.append([(new_rank, new_file)])
        return paths