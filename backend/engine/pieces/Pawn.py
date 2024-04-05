from engine.piece import Piece
from engine.constants import COLOR, MAX_FILE, PAWN_START

class Pawn(Piece):
    def __init__(self, rank, file, color):
        super().__init__(rank, file, color)
        self.initial_position = self.rank == PAWN_START["BLACK"] or self.rank == PAWN_START["WHITE"]
        self.name = 'p' if color == COLOR['BLACK'] else 'P'

    def can_move(self, to_pos, is_capture=False):
        to_rank, to_file = to_pos

        if not super().can_move(to_pos):
            return False

        rank_difference = abs(self.rank - to_rank)
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

    def get_possible_paths(self,):
        paths = []
        direction = -1 if self.color == COLOR["WHITE"] else 1
        start_rank = PAWN_START["WHITE"] if self.color == COLOR["WHITE"] else PAWN_START["BLACK"]

        forward_path = [(self.rank + direction, self.file)]
        if self.rank == start_rank:
            forward_path.append((self.rank + 2 * direction, self.file))
        paths.append(forward_path)

        for d_file in [-1, 1]:
            new_file = self.file + d_file
            if 1 <= new_file <= MAX_FILE:
                capture_path = [(self.rank + direction, new_file)]
                paths.append(capture_path)

        return paths
