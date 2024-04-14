from engine.piece import Piece
from engine.constants import COLOR, MAX_RANK
from engine.Position import Position

class Queen(Piece):
    def __init__(self, position: Position, color: str) -> None:
        super().__init__(position, color)
        self.name = 'q' if color == COLOR['BLACK'] else 'Q'
        self.symbol = "♕" if color == COLOR["WHITE"] else "♛"
        
    def can_move(self, to_pos: Position):
        to_rank, to_file = to_pos.rank, to_pos.file

        if not super().can_move(to_pos): 
            return False

        same_rank = self.position.rank == to_rank
        same_file = self.position.file == to_file


        rank_difference = abs(self.position.rank - to_rank)
        file_difference = abs(self.position.file - to_file)

        return (same_rank != same_file) or (rank_difference == file_difference)

    def get_possible_paths(self):
        paths = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]

        for d_rank, d_file in directions:
            path = []
            for step in range(1, MAX_RANK):
                new_rank = self.position.rank + step * d_rank
                new_file = self.position.file + step * d_file
                new_position = Position(rank=new_rank, file=new_file)
                if new_position.is_on_board():
                    path.append(new_position)
                else:
                    break
            if path:
                paths.append(path)
        return paths