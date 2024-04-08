from engine.constants import MAX_RANK, MAX_FILE

def visualize_possible_moves(possible_moves, piece_position, piece_name):
    if possible_moves is None: 
        return
    for rank in range(1, MAX_RANK + 1):
        for file in range(1, MAX_FILE + 1):
            if (rank, file) == piece_position:
                print(f" {piece_name} ", end="")
            elif (rank, file) in possible_moves:
                print(" X ", end="")
            else:
                print(" . ", end="")
        print()
    
def lists_equal(lst1, lst2):
    if not lst1 and lst2: return False
    if not lst2 and lst1: return False
    if not lst1 and not lst2: return True 
    if len(lst1) != len(lst2): return False 
    
    if (isinstance(lst1[0], list)):
        equal = False 
        for a, b in zip(lst1, lst2):
            if len(a) != len(b): 
                equal = False 
                break
            equal = sorted(a) == sorted(b)
        equal = sorted(lst1) == sorted(lst2)
        return equal 
    
    return sorted(lst1) == sorted(lst2)
        