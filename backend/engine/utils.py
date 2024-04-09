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
    
def lists_equal(lst1, lst2, verbose=False):
    if not lst1 and lst2: 
        if verbose:
            print(f"List 1 is empty but list 2 is not empty = {lst2}")
        return False
    if not lst2 and lst1: 
        if verbose:
            print(f"List 1 is not empty = {lst1} but list 2 is empty.")
        return False
    if not lst1 and not lst2: 
        return True 
    if len(lst1) != len(lst2): 
        if verbose:
            print(f"Length of list 1 = {len(lst1)} != Length of list 2 = {len(lst2)}.")
        return False 
    
    if (isinstance(lst1[0], list)):
        equal = False 
        for a, b in zip(lst1, lst2):
            if len(a) != len(b): 
                equal = False 
                break
            equal = sorted(a) == sorted(b)
            if not equal:
                if verbose:
                    print(f"{sorted(a)} != {sorted(b)}")
        equal = sorted(lst1) == sorted(lst2)
        return equal 
    
    return sorted(lst1) == sorted(lst2)


def algebraic_to_coords(algebraic_notation):
    file_to_num = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}

    file_letter = algebraic_notation[0]
    rank_number = 9 - int(algebraic_notation[1])

    file_number = file_to_num[file_letter]

    return (rank_number, file_number)
        