from engine.piece import Piece
from engine.constants import *


class Queen(Piece):
    def __init__(self, rank, file, color) -> None:
        super().__init__(rank, file, color)
        self.name = 'q' if color == COLOR['BLACK'] else 'Q'


    def can_move(self, to_pos):
        to_rank, to_file = to_pos

        if not super().can_move(to_pos): return False

        same_rank = self.rank == to_rank
        same_file = self.file == to_file


        rank_difference = abs(self.rank - to_rank)
        file_difference = abs(self.file - to_file)

        return (same_rank != same_file) or (rank_difference == file_difference)

    def get_possible_paths(self):
        paths = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]

        for d_rank, d_file in directions:
            path = []
            for step in range(1, max(MAX_RANK, MAX_FILE)):
                new_rank = self.rank + step * d_rank
                new_file = self.file + step * d_file
                if 1 <= new_rank <= MAX_RANK and 1 <= new_file <= MAX_FILE:
                    path.append((new_rank, new_file))
                else:
                    break
            if path:
                paths.append(path)
        return paths