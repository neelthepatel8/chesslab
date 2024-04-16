from engine.constants import MAX_RANK, MAX_FILE

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
        outer_equal = False 
        for a, b in zip(lst1, lst2):
            if len(a) != len(b): 
                equal = False 
                break
            equal = False
            for each, each2 in zip(a, b):
                if each != each2:
                    equal = False
            if not equal:
                if verbose:
                    print(f"{a} != {b}")
        equal = sorted(lst1) == sorted(lst2)
        return equal 
    
    return sorted(lst1) == sorted(lst2)


def algebraic_to_coords(algebraic_notation):
    file_to_num = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}

    file_letter = algebraic_notation[0]
    rank_number = 9 - int(algebraic_notation[1])

    file_number = file_to_num[file_letter]

    return (rank_number, file_number)


def boards_equal(board1, board2, verbose=False):
    if verbose:
        print()
    if len(board1) != len(board2):
        if verbose:
            print(f"Size of boards dont match: board1: {len(board1)} != board2: {len(board2)}")
        return False

    for r_index, (row1, row2) in enumerate(zip(board1, board2)):
        for c_index, (each1, each2) in enumerate(zip(row1, row2)):
            if each1 != each2:
                if verbose:
                    print(f"Square mismatch, {r_index}, {c_index} {each1} != {each2}")
                return False

    return True

    
        