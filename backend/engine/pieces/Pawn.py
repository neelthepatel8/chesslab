from engine.piece import Piece
from engine.constants import COLOR, MAX_FILE, PAWN_START
from engine.utils import algebraic_to_coords
class Pawn(Piece):
    def __init__(self, rank, file, color) -> None:
        super().__init__(rank, file, color)
        self.initial_position = self.rank == PAWN_START["BLACK"] or self.rank == PAWN_START["WHITE"]
        self.name = 'p' if color == COLOR['BLACK'] else 'P'

    def can_move(self, to_pos) -> bool:

        to_rank, to_file = -1, -1
        if isinstance(to_pos, str):
            # Move is in algebraic notation
            to_rank, to_file = algebraic_to_coords(to_pos)
        else:
            # Move is in coordinates form
            to_rank, to_file = to_pos 
        
        if to_rank == -1 or to_file == -1:
            return False 

        # If different file, move not possible
        if self.file != to_file:
            return False
        

        rank_difference = self.rank - to_rank
        
        # Trying to move 2 Squares has to be in initial position and relevant colors for direction
        if rank_difference == 2:
            if self.initial_position:
                if self.color == COLOR["WHITE"]:
                    return True
        
        if rank_difference == -2:
            if self.initial_position:
                if self.color == COLOR["BLACK"]:
                    return True

        
        # Trying to move 1 square, just need to check relevant colors for direction
        if rank_difference == 1:
            if self.color == COLOR["WHITE"]:
                return True
        
        if rank_difference == -1:
            if self.color == COLOR["BLACK"]:
                return True
        
        # If not 1 block or 2 block move, illeagal move.
        return False
    
    def can_kill(self, to_pos):
        if self.can_move(to_pos):
            return False
        
        to_rank, to_file = -1, -1
        if isinstance(to_pos, str):
            # Kill is in algebraic notation
            to_rank, to_file = algebraic_to_coords(to_pos)
        else:
            # Kill is in coordinates form
            to_rank, to_file = to_pos 
        
        if to_rank == -1 or to_file == -1:
            return False 


        rank_difference = self.rank - to_rank
        file_difference = self.file - to_file

        # Cannot kill sideways
        if rank_difference == 0 or file_difference == 0:
            return False

        # Cannot kill more than 1 block away
        if rank_difference >= 2 or file_difference >= 2:
            return False
        
        if self.color == COLOR["WHITE"] and rank_difference == 1:
            return True
    
        if self.color == COLOR["BLACK"] and rank_difference == -1:
            return True
        
        return False
           
    def get_all_moves(self) -> set:
        all_moves = self.get_possible_paths()
        return set(all_moves)

    def get_possible_paths(self) -> list:
        paths = []
        direction = -1 if self.color == COLOR["WHITE"] else 1

        if self.check_bounds(self.rank + direction):
            paths.append([(self.rank + direction, self.file)])

        if self.initial_position:
            if self.check_bounds(self.rank + direction * 2):
                paths.append([(self.rank + direction, self.file), (self.rank + direction * 2, self.file)])

        return paths
    