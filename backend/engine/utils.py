from engine.constants import *

def visualize_possible_moves(possible_moves, piece_position, piece_name):
    if possible_moves == None: return
    for rank in range(1, MAX_RANK + 1):
        for file in range(1, MAX_FILE + 1):
            if (rank, file) == piece_position:
                print(f" {piece_name} ", end="")
            elif (rank, file) in possible_moves:
                print(" X ", end="")
            else:
                print(" . ", end="")
        print()