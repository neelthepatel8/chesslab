from engine.Position import Position
import engine.fen_utils as fen_utils 
import engine.bitmanipulation.bitwise as bitwise
from engine.piece import Piece
from engine.constants import WHITE, BLACK, PIECE_REPRESENTATION
import engine.pieces as pieces
from engine.FastBoard.PieceList import PieceList

PAWN = 1
BISHOP = 2
QUEEN = 3
KNIGHT = 4
ROOK = 5
KING = 6
NULL = -1

EMPTY = 0
UNIVERSE = 1

class FastBoard():
    def __init__(self) -> None:
        self.pieces = PieceList([32768, 16384, 8192, 4096, 2048, 1024, 512, 256, 64, 2, 32, 4, 128, 1, 16, 8, 
                       36028797018963968, 18014398509481984, 9007199254740992, 4503599627370496,
                       2251799813685248, 1125899906842624, 562949953421312, 281474976710656,
                       4611686018427387904, 144115188075855872, 2305843009213693952,
                       288230376151711744, 9223372036854775808, 72057594037927936,
                       1152921504606846976, 576460752303423488])
        
        self.active = WHITE
        
        # Occupancy bitboards
        self.pieceTypes = [0] * 6
        self.colors = [0, 0]
        self.occupied = 0
        
        
        for piece, pieceType, pieceColor in self.pieces:
            self.pieceTypes[pieceType] |= piece
            self.colors[pieceColor] |= piece
            self.occupied |= piece

    def get_piece(self, position: Position) -> Piece | None:
        piece_details = self.piece_details(position)
        if piece_details is None:
            return None
        
        color, piece_type = piece_details
        piece = self.make_piece(color, piece_type, position)
        return piece 
    
    def make_piece(self, color: int, piece_type: int, position: Position) -> Piece:
        if piece_type == PAWN:
            return pieces.Pawn(position, color)
        if piece_type == BISHOP:
            return pieces.Bishop(position, color)
        if piece_type == KNIGHT:
            return pieces.Knight(position, color)
        if piece_type == ROOK:
            return pieces.Rook(position, color)
        if piece_type == QUEEN:
            return pieces.Queen(position, color)
        if piece_type == KING:
            return pieces.King(position, color)
        
        return None

    def piece_details(self, position):
        index = 63 - self.position_to_index(position)
        for color, color_bitboards in self.bitboards.items():
            for piece_type, bitboard in color_bitboards.items():
                if piece_type != NULL:
                    if bitwise.get_bit(bitboard, index):
                        return color, piece_type
            
        return None
    
    def position_to_index(self, position: Position) -> int:
        rank, file = position.lsrcoords
        print("Pos: ", rank, file)
        index = rank * 8 + file 
        return index
    
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

        
                    
            
                                

