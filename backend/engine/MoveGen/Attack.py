import engine.bitboard.bitwise as bitwise
from engine.bitboard.utils import show_raw
from engine.constants import COLOR


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

def bishop():
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

def rook():
    return [rook_at(i) for i in range(64)]

