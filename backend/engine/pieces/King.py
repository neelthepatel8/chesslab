from engine.piece import Piece
from engine.constants import *


class King(Piece):
    def __init__(self, rank, file, color) -> None:
        super().__init__(rank, file, color)
        self.name = 'k' if color == COLOR['BLACK'] else 'K'


    def can_move(self, to_pos):
        to_rank, to_file = to_pos

        if not super().can_move(to_pos):
            return False

        rank_difference = abs(self.rank - to_rank)
        file_difference = abs(self.file - to_file)

        return (rank_difference <= 1) and (file_difference <= 1)

    def get_possible_paths(self):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]
        paths = []

        for d_rank, d_file in directions:
            new_rank = self.rank + d_rank
            new_file = self.file + d_file
            if 1 <= new_rank <= MAX_RANK and 1 <= new_file <= MAX_FILE:
                paths.append([(new_rank, new_file)])
        return paths
