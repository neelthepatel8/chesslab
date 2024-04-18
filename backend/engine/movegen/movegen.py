def knight():
    moves = {}
    board_size = 8
    knight_offsets = [-17, -15, -10, -6, 6, 10, 15, 17]
    for index in range(64):
        move_bitmask = 0
        x, y = index % board_size, index // board_size
        for offset in knight_offsets:
            nx, ny = x + offset % board_size, y + offset // board_size
            if 0 <= nx < board_size and 0 <= ny < board_size:
                new_index = ny * board_size + nx
                move_bitmask |= (1 << new_index)
        moves[index] = move_bitmask
    return moves

def rook():
    moves = {}
    board_size = 8
    rook_offsets = [-8, 1, 8, -1]  
    for index in range(64):
        move_bitmask = 0
        x, y = index % board_size, index // board_size
        for offset in rook_offsets:
            for step in range(1, board_size):
                nx, ny = x + (offset % board_size) * step, y + (offset // board_size) * step
                if 0 <= nx < board_size and 0 <= ny < board_size:
                    new_index = ny * board_size + nx
                    move_bitmask |= (1 << new_index)
                else:
                    break
        moves[index] = move_bitmask
    return moves

def bishop():
    moves = {}
    board_size = 8
    bishop_offsets = [-9, -7, 7, 9] 
    for index in range(64):
        move_bitmask = 0
        x, y = index % board_size, index // board_size
        for offset in bishop_offsets:
            for step in range(1, board_size):
                nx, ny = x + (offset % board_size) * step, y + (offset // board_size) * step
                if 0 <= nx < board_size and 0 <= ny < board_size:
                    new_index = ny * board_size + nx
                    move_bitmask |= (1 << new_index)
                else:
                    break
        moves[index] = move_bitmask
    return moves

def queen():
    moves = {}
    board_size = 8
    queen_offsets = [-9, -8, -7, -1, 1, 7, 8, 9]  
    for index in range(64):
        move_bitmask = 0
        x, y = index % board_size, index // board_size
        for offset in queen_offsets:
            for step in range(1, board_size):
                nx, ny = x + (offset % board_size) * step, y + (offset // board_size) * step
                if 0 <= nx < board_size and 0 <= ny < board_size:
                    new_index = ny * board_size + nx
                    move_bitmask |= (1 << new_index)
                else:
                    break
        moves[index] = move_bitmask
    return moves

def king():
    moves = {}
    board_size = 8
    king_offsets = [-9, -8, -7, -1, 1, 7, 8, 9] 
    for index in range(64):
        move_bitmask = 0
        x, y = index % board_size, index // board_size
        for offset in king_offsets:
            nx, ny = x + offset % board_size, y + offset // board_size
            if 0 <= nx < board_size and 0 <= ny < board_size:
                new_index = ny * board_size + nx
                move_bitmask |= (1 << new_index)
        moves[index] = move_bitmask
    return moves


