from engine.piece import Piece
from engine.constants import *

class Bishop(Piece):
    def __init__(self, rank, file, color) -> None:
        super().__init__(rank, file, color)
        self.name = 'b' if color == COLOR['BLACK'] else 'B'

    def can_move(self, to_pos):
        to_rank, to_file = to_pos

        if not super().can_move(to_pos):
            return False

        rank_difference = abs(self.rank - to_rank)
        file_difference = abs(self.file - to_file)

        return rank_difference == file_difference

    def get_possible_paths(self):
        paths = []
        directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]

        for d_rank, d_file in directions:
            path = []
            for step in range(1, MAX_RANK):
                new_rank = self.rank + step * d_rank
                new_file = self.file + step * d_file

                if 1 <= new_rank <= MAX_RANK and 1 <= new_file <= MAX_FILE:
                    path.append((new_rank, new_file))
                else:
                    break
            if path:
                paths.append(path)

        return paths