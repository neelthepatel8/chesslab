from piece import Piece
from constants import *

class Pawn(Piece):
    def __init__(self, rank, file, color):
        super().__init__(rank, file, color)
        self.initial_position = self.rank == PAWN_START["BLACK"] or self.rank == PAWN_START["WHITE"]
        self.name = 'p' if color == COLOR['BLACK'] else 'P'

    def can_move(self, to_pos, is_capture=False):
        to_rank, to_file = to_pos

        if not super().can_move(to_pos):
            return False

        rank_difference = self.rank - to_rank if self.color == COLOR["WHITE"] else to_rank - self.rank
        file_difference = abs(self.file - to_file)

        if not is_capture:
            if rank_difference == 1 and file_difference == 0:
                return True
            elif self.initial_position and rank_difference == 2 and file_difference == 0:
                return True
        else:
            if rank_difference == 1 and file_difference == 1:
                return True

        return False

    def can_kill(self, to_pos):
        return self.can_move(to_pos, is_capture=True)

    def get_possible_paths(self):
        paths = []
        direction = 1 if self.color == COLOR["WHITE"] else -1
        start_rank = 2 if self.color == COLOR["WHITE"] else 7

        if self.rank == start_rank:
            paths.append([(self.rank + direction, self.file), (self.rank + 2 * direction, self.file)])
        else:
            paths.append([(self.rank + direction, self.file)])

        for d_file in [-1, 1]:
            new_file = self.file + d_file
            if 1 <= new_file <= MAX_FILE:
                paths.append([(self.rank + direction, new_file)])

        return paths