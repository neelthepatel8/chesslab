from constants import *

class Piece():
    def __init__(self, rank, file, color) -> None:

        if rank > MAX_RANK or rank < MIN_RANK or file > MAX_FILE or file < MIN_FILE:
            raise ValueError("Piece cannot be outside the board! Please use values between 1 - 8")

        self.rank = rank
        self.file = file
        self.color = color

    def can_move(self, to_pos):

        if (self.rank, self.file) == to_pos: return False

        to_rank, to_file = to_pos

        rank_check = MIN_RANK <= to_rank <= MAX_RANK
        file_check = MIN_FILE <= to_file <= MAX_FILE

        return rank_check and file_check

    def can_kill(self, to_pos):
        return self.can_move(to_pos)

    def get_possible_moves(self):

        possible_moves = []

        for to_rank in range(1, MAX_RANK + 1):
            for to_file in range(1, MAX_FILE + 1):
                if self.can_move((to_rank, to_file)):
                    possible_moves.append((to_rank, to_file))

        return possible_moves

    def get_name(self):
        return self.name

    def get_color(self):
        return self.color
