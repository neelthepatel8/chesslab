from engine.piece import Piece
from engine.constants import COLOR, PAWN_START
from engine.Position import Position
class Pawn(Piece):
    def __init__(self, position: Position, color: str) -> None:
        super().__init__(position, color)
        self.initial_position = self.position.rank == PAWN_START["BLACK"] or self.position.rank == PAWN_START["WHITE"]
        self.name = 'p' if color == COLOR['BLACK'] else 'P'

    def can_move(self, to_pos: Position) -> bool:

        to_rank, to_file = to_pos.rank, to_pos.file

        # If different file, move not possible
        if self.position.file != to_file:
            return False
        

        rank_difference = self.position.rank - to_rank
        
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
    
    def can_kill(self, to_pos: Position):
        if self.can_move(to_pos):
            return False
        
        to_rank, to_file = to_pos.rank, to_pos.file

        rank_difference = self.position.rank - to_rank
        file_difference = self.position.file - to_file

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

        if self.check_bounds(self.position.rank + direction):
            new_position = Position(rank=self.position.rank + direction, file=self.position.file)
            paths.append([new_position])

        if self.initial_position:
            if self.check_bounds(self.position.rank + direction * 2):
                one_step = Position(rank=self.position.rank + direction, file=self.position.file)
                two_step = Position(rank=self.position.rank + direction * 2, file=self.position.file)
                
                paths.append([one_step, two_step])

        return paths
    