import engine.bitmanipulation.bitwise as bitwise
from engine.bitmanipulation.utils import count_bits, show_raw
from engine.constants import COLOR
from engine.MoveGen.magic import ROOK_MAGICS, BISHOP_MAGICS

ROOK_MASKS = None
ROOK_MOVES = None

BISHOP_MASKS = None
BISHOP_MOVES = None

ROOK_SHIFTS = None
BISHOP_SHIFTS = None

ROOK_INDEX_BITS = None 
BISHOP_INDEX_BITS = None

not_h_file = 9187201950435737471
not_a_file = 18374403900871474942
not_hg_file = 4557430888798830399
not_ab_file = 18229723555195321596


file_mask_a = 72340172838076673
file_mask_b = 144680345676153346
file_mask_c = 289360691352306692
file_mask_d = 578721382704613384
file_mask_e = 1157442765409226768
file_mask_f = 2314885530818453536
file_mask_g = 4629771061636907072
file_mask_h = 9259542123273814144

rank_mask_0 = 18374686479671623680
rank_mask_1 = 71776119061217280
rank_mask_2 = 280375465082880
rank_mask_3 = 1095216660480
rank_mask_4 = 4278190080
rank_mask_5 = 16711680
rank_mask_6 = 65280
rank_mask_7 = 255

def king_at(index: int) -> int:
    
    attacks = 0
    
    bitboard = 0
    
    bitboard = bitwise.set_bit(bitboard, index)
    
    # Up 
    if bitwise.lshift(bitboard, 8):
        attacks |= bitwise.lshift(bitboard, 8)
    
    # Down
    if bitwise.rshift(bitboard, 8):
        attacks |= bitwise.rshift(bitboard, 8)
        
    # Right
    if bitwise.lshift(bitboard, 1) & not_a_file:
        attacks |= bitwise.lshift(bitboard, 1)
        
    # Left
    if bitwise.rshift(bitboard, 1) & not_h_file:
        attacks |= bitwise.rshift(bitboard, 1)
        
    # Top left
    if bitwise.rshift(bitboard, 7) & not_a_file:
        attacks |= bitwise.rshift(bitboard, 7)
        
    # Top right
    if bitwise.rshift(bitboard, 9) & not_h_file:
        attacks |= bitwise.rshift(bitboard, 9)
    
    # Bottom left
    if bitwise.lshift(bitboard, 9) & not_a_file :
        attacks |= bitwise.lshift(bitboard, 9)
        
    # Bottom right
    if bitwise.lshift(bitboard, 7) & not_h_file:
        attacks |= bitwise.lshift(bitboard, 7)
    
    return attacks
    
def king():
    return [king_at(i) for i in range(64)]

def knight_at(index: int) -> int:
    
    attacks = 0
    
    bitboard = 0
    
    bitboard = bitwise.set_bit(bitboard, index)
    
    if bitwise.rshift(bitboard, 6) & not_ab_file:
        attacks |= bitwise.rshift(bitboard, 6)
    
    if bitwise.rshift(bitboard, 10) & not_hg_file:
        attacks |= bitwise.rshift(bitboard, 10)
    
    if bitwise.rshift(bitboard, 15) & not_a_file:
        attacks |= bitwise.rshift(bitboard, 15)
    
    if bitwise.rshift(bitboard, 17) & not_h_file:
        attacks |= bitwise.rshift(bitboard, 17)
   
    if bitwise.lshift(bitboard, 6) & not_hg_file:
        attacks |= bitwise.lshift(bitboard, 6)
        
    if bitwise.lshift(bitboard, 10) & not_ab_file:
        attacks |= bitwise.lshift(bitboard, 10)
    
    if bitwise.lshift(bitboard, 15) & not_h_file :
        attacks |= bitwise.lshift(bitboard, 15)
        
    if bitwise.lshift(bitboard, 17) & not_a_file:
        attacks |= bitwise.lshift(bitboard, 17)
    
    return attacks

def knight():
    return [knight_at(i) for i in range(64)]

def pawn_at(index: int, color: str) -> int:
    
    attacks = 0
    
    bitboard = 0
    
    bitboard = bitwise.set_bit(bitboard, index)
    
    if color == COLOR["BLACK"]:
        if bitwise.rshift(bitboard, 7) & not_a_file:
            attacks |= bitwise.rshift(bitboard, 7)
        if bitwise.rshift(bitboard, 9) & not_h_file:
            attacks |= bitwise.rshift(bitboard, 9)
    
    else:
        if bitwise.lshift(bitboard, 7) & not_h_file:
            attacks |= bitwise.lshift(bitboard, 7)
        if bitwise.lshift(bitboard, 9) & not_a_file:
            attacks |= bitwise.lshift(bitboard, 9)
    
    return attacks

def pawn(color: str):
    return [pawn_at(i, color) for i in range(64)]

def bishop_at(index: int) -> int:
    
    attacks = 0
    
    tr, tf = index // 8, index % 8
    for r, f in zip(range(tr + 1, 7), range(tf + 1, 7)):
        attacks |= bitwise.lshift(1, (r * 8 + f))
        
    for r, f in zip(range(tr - 1, 0, -1), range(tf + 1, 7)):
        attacks |= bitwise.lshift(1, (r * 8 + f))
        
    for r, f in zip(range(tr + 1, 7), range(tf - 1, 0, -1)):
        attacks |= bitwise.lshift(1, (r * 8 + f))
        
    for r, f in zip(range(tr - 1, 0, -1), range(tf - 1, 0, -1)):
        attacks |= bitwise.lshift(1, (r * 8 + f))
        
        
    return attacks

def bishop_at_relative(index: int, board: int) -> int:
    
    attacks = 0
    
    tr, tf = index // 8, index % 8
    for r, f in zip(range(tr + 1, 8), range(tf + 1, 8)):
        attacks |= bitwise.lshift(1, (r * 8 + f))
        if bitwise.lshift(1, (r * 8 + f)) & board:
            break
        
    for r, f in zip(range(tr - 1, -1, -1), range(tf + 1, 8)):
        attacks |= bitwise.lshift(1, (r * 8 + f))
        if bitwise.lshift(1, (r * 8 + f)) & board:
            break
        
    for r, f in zip(range(tr + 1, 8), range(tf - 1, -1, -1)):
        attacks |= bitwise.lshift(1, (r * 8 + f))
        if bitwise.lshift(1, (r * 8 + f)) & board:
            break
        
    for r, f in zip(range(tr - 1, -1, -1), range(tf - 1, -1, -1)):
        attacks |= bitwise.lshift(1, (r * 8 + f))
        if bitwise.lshift(1, (r * 8 + f)) & board:
            break
        
    return attacks

def bishop_masks():
    return [bishop_at(i) for i in range(64)]

def rook_at(index: int) -> int:
    
    attacks = 0
    
    tr, tf = index // 8, index % 8
    for r in range(tr + 1, 7):
        attacks |= bitwise.lshift(1, (r * 8 + tf))
    for r in range(tr - 1, 0, -1):
        attacks |= bitwise.lshift(1, (r * 8 + tf))
    for f in range(tf + 1, 7):
        attacks |= bitwise.lshift(1, (tr * 8 + f))
    for f in range(tf - 1, 0, -1):
        attacks |= bitwise.lshift(1, (tr * 8 + f))
        
        
    return attacks

def rook_at_relative(index: int, board: int) -> int:
    
    attacks = 0
    
    tr, tf = index // 8, index % 8
    for r in range(tr + 1, 8):
        attacks |= bitwise.lshift(1, (r * 8 + tf))
        if bitwise.lshift(1, (r * 8 + tf)) & board:
            break
        
    for r in range(tr - 1, -1, -1):
        attacks |= bitwise.lshift(1, (r * 8 + tf))
        if bitwise.lshift(1, (r * 8 + tf)) & board:
            break
        
    for f in range(tf + 1, 8):
        attacks |= bitwise.lshift(1, (tr * 8 + f))
        if bitwise.lshift(1, (tr * 8 + f)) & board:
            break
        
    for f in range(tf - 1, -1, -1):
        attacks |= bitwise.lshift(1, (tr * 8 + f))
        if bitwise.lshift(1, (tr * 8 + f)) & board:
            break
        
    return attacks

def rook_masks():
    return [rook_at(i) for i in range(64)]

def generate_blocker_configurations(mask: int):
    n = count_bits(mask)
    for i in range(bitwise.lshift(1, n)):
        blockers = 0
        k = 0
        for j in range(64):
            if mask & bitwise.lshift(1, j):
                if i & bitwise.lshift(1, k):
                    blockers |= bitwise.lshift(1, j)
                k += 1
        yield blockers

def compute_rook_moves(square: int, blockers: int):
    moves = 0
    directions = [1, -1, 8, -8] 
    for direction in directions:
        pos = square
        while True:
            pos += direction
            if not (0 <= pos < 64): 
                break
            if (direction == 1 and pos % 8 == 0): 
                break
            if (direction == -1 and pos % 8 == 7): 
                break
            moves |= bitwise.lshift(1, pos)
            if blockers & bitwise.lshift(1, pos): 
                break
    return moves



def rook_lookup_table():
    rook_moves = [None] * 64
    for square in range(64):
        mask = ROOK_MASKS[square]
        magic = ROOK_MAGICS[square]
        shift_amount = 64 - count_bits(mask)  
        size = 2 ** count_bits(mask)
        rook_moves[square] = [0] * size
        for blockers in generate_blocker_configurations(mask):
            index = bitwise.rshift((blockers * magic), shift_amount)
            index = index & (size - 1)  
            rook_moves[square][index] = compute_rook_moves(square, blockers)
    return rook_moves

def compute_bishop_moves(square: int, blockers: int):
    moves = 0
    directions = [9, 7, -9, -7]  
    for direction in directions:
        pos = square
        while True:
            pos += direction
            if not (0 <= pos < 64):
                break
            if (direction == 9 or direction == -7) and pos % 8 == 0:  
                break
            if (direction == 7 or direction == -9) and pos % 8 == 7: 
                break
            moves |= bitwise.lshift(1, pos)
            if blockers & bitwise.lshift(1, pos):
                break
    return moves

def bishop_lookup_table():
    bishop_moves = [None] * 64
    for square in range(64):
        mask = BISHOP_MASKS[square]  
        magic = BISHOP_MAGICS[square] 
        shift_amount = 64 - count_bits(mask)  
        size = 2 ** count_bits(mask)
        bishop_moves[square] = [0] * size
        for blockers in generate_blocker_configurations(mask):
            index = bitwise.rshift((blockers * magic), shift_amount)
            index = index & (size - 1) 
            bishop_moves[square][index] = compute_bishop_moves(square, blockers)
    return bishop_moves


def shifts(masks: int):
    shifts = []
    for mask in masks:
        index_bits = count_bits(mask)
        shift = 64 - index_bits
        shifts.append(shift)
    return shifts

def rook_move(index: int, board: int):
    blockers = board & ROOK_MASKS[index]
    index_bits = ROOK_INDEX_BITS[index]  
    index_mask = bitwise.lshift(1, index_bits) - 1
    magic_index = bitwise.rshift((blockers * ROOK_MAGICS[index]), ROOK_SHIFTS[index])
    safe_index = magic_index & index_mask
    return ROOK_MOVES[index][safe_index]

def bishop_move(index: int, board: int):
    blockers = board & BISHOP_MASKS[index]
    index_bits = BISHOP_INDEX_BITS[index]  
    index_mask = bitwise.lshift(1, index_bits) - 1
    magic_index = bitwise.rshift((blockers * BISHOP_MAGICS[index]), BISHOP_SHIFTS[index])
    safe_index = magic_index & index_mask
    return BISHOP_MOVES[index][safe_index]


def init():
    global ROOK_MASKS, BISHOP_MASKS, ROOK_MOVES, BISHOP_MOVES, ROOK_SHIFTS, BISHOP_SHIFTS, ROOK_INDEX_BITS, BISHOP_INDEX_BITS

    ROOK_MASKS = rook_masks()
    BISHOP_MASKS = bishop_masks()

    ROOK_MOVES = rook_lookup_table()
    BISHOP_MOVES = bishop_lookup_table()

    ROOK_INDEX_BITS = [count_bits(ROOK_MASKS[i]) for i in range(64)]
    BISHOP_INDEX_BITS = [count_bits(BISHOP_MASKS[i]) for i in range(64)]

    ROOK_SHIFTS = shifts(ROOK_MASKS)
    BISHOP_SHIFTS = shifts(BISHOP_MASKS)