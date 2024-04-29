from engine.constants import WHITE, PIECE_REPRESENTATION
from engine.FastBoard.PieceList import PieceList

class FastBoard():
    def __init__(self, active=WHITE, pieces=None) -> None:
        self.pieces = pieces
        
        if pieces is None:
            self.pieces = PieceList([32768, 16384, 8192, 4096, 2048, 1024, 512, 256, 64, 2, 32, 4, 128, 1, 16, 8, 
                        36028797018963968, 18014398509481984, 9007199254740992, 4503599627370496,
                        2251799813685248, 1125899906842624, 562949953421312, 281474976710656,
                        4611686018427387904, 144115188075855872, 2305843009213693952,
                        288230376151711744, 9223372036854775808, 72057594037927936,
                        1152921504606846976, 576460752303423488])
        
        self.active = active
        
        # Occupancy bitboards
        self.pieceTypes = [0] * 6
        self.colors = [0, 0]
        self.occupied = 0
        
        
        for piece, pieceType, pieceColor in self.pieces:
            self.pieceTypes[pieceType] |= piece
            self.colors[pieceColor] |= piece
            self.occupied |= piece

    def __add__(self, move):
        return self._update(move)
    
    def __sub__(self, move):
        return self._update(move, reverse=True)

    def _update(self, move, reverse=False):
        p0, p1 = (move.end, move.start) if reverse else (move.start, move.end)
        color = not self.active if reverse else self.active

        self.pieces.update(p0, p1, color)

        self.pieceTypes[move.pieceType] &= ~p0
        self.colors[color] &= ~p0

        self.pieceTypes[move.pieceType] |= p1
        self.colors[color] |= p1

        is_capture = move.captureType is not None
        

        if reverse and is_capture:
            self.pieces.insert(p0, move.captureType, not color)
            self.pieceTypes[move.captureType] |= p0
            self.colors[not color] |= p0
        
        elif is_capture:
            self.pieces.remove(p1, not color)
            self.colors[not color] &= ~p1
            if move.pieceType != move.captureType:
                self.pieceTypes[move.captureType] &= ~p1

        self.occupied = self.colors[0] | self.colors[1]

        self.active = not self.active

        return self
    
    def get_piece_type(self, piece):
        for pieceType, pieceSet in enumerate(self.pieceTypes):
            if piece & pieceSet != 0:
                return pieceType
        raise RuntimeError('Could not find piece type')

    def __str__(self):
        squares = ['.'] * 64  
        for piece, pieceType, color in self.pieces:
            isBitOn = lambda index: piece & (1 << (63-index)) != 0
            square = list(map(isBitOn, range(64))).index(True)
            squares[square] = PIECE_REPRESENTATION[color][pieceType]
        formatRow = lambda r: '87654321'[r//8] + ' '.join(squares[r:r+8])
        return '\n'.join(map(formatRow, range(0, 64, 8))) + '\n a b c d e f g h'

        
                    
            
                                

