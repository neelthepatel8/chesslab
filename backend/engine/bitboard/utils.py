from engine.bitboard.bitwise import get_bit

def show_raw(board: int) -> None:
    board_str = f"{board:064b}"
    print(board_str)
    for i in range(0, 64, 8):
        print(board_str[i:i+8][::-1])
    
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
