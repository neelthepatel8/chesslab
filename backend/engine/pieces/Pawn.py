from engine.piece import Piece
from engine.constants import COLOR, PAWN_START
from engine.Position import Position
class Pawn(Piece):
    def __init__(self, position: Position, color: str) -> None:
        super().__init__(position, color)
        self.initial_position = self.is_initial_position()
        self.name = 'p' if color == COLOR['BLACK'] else 'P'
        self.symbol = "♙" if color == COLOR["WHITE"] else "♟︎"
        self.value = 1.0
        self.positional_values = [
            [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
            [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
            [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
            [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
            [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
            [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
            [0.5,  1.0,  1.0,  -2.0, -2.0,  1.0,  1.0,  0.5],
            [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
        ]
        
        self.positional_values = list(reversed(self.positional_values)) if color == COLOR["BLACK"] else self.positional_values
        
    def is_initial_position(self):
        return self.position.rank == PAWN_START["BLACK"] or self.position.rank == PAWN_START["WHITE"]
        
    def can_move(self, to_pos: Position) -> bool:
        rank_difference = to_pos.rank - self.position.rank
        file_difference = to_pos.file - self.position.file

        direction = -1 if self.color == COLOR["WHITE"] else 1 

        if file_difference == 0:
            if (rank_difference == direction): 
                return True
            if (rank_difference == 2 * direction and self.is_initial_position()): 
                return True

        return False

    def can_kill(self, to_pos: Position):
        rank_difference = to_pos.rank - self.position.rank
        file_difference = to_pos.file - self.position.file

        direction = -1 if self.color == COLOR["WHITE"] else 1

        if abs(file_difference) == 1 and rank_difference == direction:
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

        if self.is_initial_position():
            if self.check_bounds(self.position.rank + direction * 2):
                one_step = Position(rank=self.position.rank + direction, file=self.position.file)
                two_step = Position(rank=self.position.rank + direction * 2, file=self.position.file)
                
                paths.append([one_step, two_step])
            
        diagonals = [(self.position.rank + direction, self.position.file - 1), (self.position.rank + direction, self.position.file + 1)]
        for r, f in diagonals:
            diagonal_position = Position(rank=r, file=f)
            if self.can_kill(diagonal_position):
                paths.append([diagonal_position])

        return paths
    