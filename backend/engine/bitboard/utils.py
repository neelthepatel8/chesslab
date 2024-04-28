from engine.bitboard.bitwise import get_bit

def show_raw(board: int) -> None:
    bin_string = f"{board:064b}"
    print(f"{board} -> {bin_string}")
    
    bin_string = bin_string[::-1]

    rows = [bin_string[i:i+8] for i in range(0, len(bin_string), 8)][::-1]
    print("  +-----------------+")

    for rank in range(8):
        print(f"{8 - rank} |", end=' ')
        print(' '.join(rows[rank]), end=" ")
        print("|")
    print("  +-----------------+")
    print("    a b c d e f g h ")

    
def show_raw_indices(board: int) -> None:
    print(f"{board} -> {board:064b}")
    print("  +-----------------+")
    for rank in reversed(range(8)): 
        print(f"{rank+1} |", end=' ')  
        for file in range(8): 
            index = rank * 8 + file
            bit = get_bit(board, index)
            print(f"{index if not bit else 'X'}", end=' ')
        print("|")
    print("  +-----------------+")
    print("    a b c d e f g h ")

    
def show(board: int) -> None:
    print(f"{board} -> {board:064b}")
    print("  +-----------------+")
    for rank in reversed(range(8)): 
        print(f"{rank+1} |", end=' ')  
        for file in range(8): 
            index = rank * 8 + file
            if get_bit(board, index):
                print("X", end=' ')
            else:
                print('.', end=' ')
        print("|")
    print("  +-----------------+")
    print("    a b c d e f g h ")

def bitmask_to_positions(bitmask: int) -> list:
    positions = []
    for i in range(64):
        if bitmask & (1 << i):
            positions.append(i)
    return positions

def count_bits(board: int) -> int:
    count = 0
    
    while board:
        count += 1
        board &= board - 1
        
    return count

def lsb(board: int) -> int:
    if board:
        return count_bits((board & -board)- 1)
    return -1