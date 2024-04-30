from engine.bitmanipulation.utils import lsb
from engine.Move import Move 
from engine.Position import Position

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

def fen_to_bitboards(fen):
    pieces_placement = fen.split(' ')[0]
    rows = pieces_placement.split('/')
    
    bitboards = [0] * 32 

    piece_count = {
        'R': 0, 'N': 0, 'B': 0, 'Q': 0, 'K': 0, 'P': 0,
        'r': 0, 'n': 0, 'b': 0, 'q': 0, 'k': 0, 'p': 0
    }

    piece_start_indices = {
        'R': 12, 'N': 8, 'B': 10, 'Q': 15, 'K': 14, 'P': 0,
        'r': 28, 'n': 24, 'b': 26, 'q': 31, 'k': 30, 'p': 16
    }

    rows.reverse()
    
    for row_index, row in enumerate(rows):
        file_index = 0
        for char in row:
            if char.isdigit():
                file_index += int(char)
            elif char.isalpha():
                current_piece_index = piece_start_indices[char] + piece_count[char]
                adjusted_file_index = 7 - file_index  # This line inverts the order
                bit_position = (8 * row_index) + adjusted_file_index
                bitboards[current_piece_index] = 1 << bit_position
                piece_count[char] += 1
                file_index += 1

    return bitboards


def bitboard_move_to_object(move):
    piece_map = {
        0: 'p',
        1: 'n',
        2: 'b',
        3: 'r',
        4: 'q',
        5: 'k'
    }
    start = Position(index=lsb(move.start))
    end = Position(index=lsb(move.end))
    print(f"Found start and end: ", move.start, lsb(move.start), lsb(move.end))
    piece_type = piece_map[move.pieceType] if move.color == 1 else piece_map[move.pieceType].upper()
    color = move.color 
    capture = move.captureType
    
    return Move(start, end, piece_type, color=color, capture=capture)
    
    
    