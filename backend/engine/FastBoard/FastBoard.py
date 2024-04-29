from engine.Position import Position
import engine.fen_utils as fen_utils 
import engine.bitmanipulation.bitwise as bitwise
from engine.piece import Piece
from engine.constants import COLOR
import engine.pieces as pieces
from engine.Move import Move

WHITE = 8
BLACK = 16

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
    def __init__(self, fen=None) -> None:
        self.bitboards = self.init()
        if fen is not None:
            self.load_fen(fen)

    def get_piece(self, position: Position) -> Piece | None:
        piece_details = self.piece_details(position)
        if piece_details is None:
            return None
        
        color, piece_type = piece_details
        piece = self.make_piece(color, piece_type, position)
        return piece 
    
    def make_piece(self, color: int, piece_type: int, position: Position) -> Piece:
        color = COLOR["BLACK"] if color == BLACK else COLOR["WHITE"]

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
    
    def init(self):
        bitboards = {
            BLACK: {
                PAWN: EMPTY,
                BISHOP: EMPTY,
                KNIGHT: EMPTY,
                ROOK: EMPTY,
                QUEEN: EMPTY,
                KING: EMPTY,
                NULL: EMPTY,
            }, 
            WHITE: {
                PAWN: EMPTY,
                BISHOP: EMPTY,
                KNIGHT: EMPTY,
                ROOK: EMPTY,
                QUEEN: EMPTY,
                KING: EMPTY,
                NULL: EMPTY,
            },
        }

        return bitboards
    
    def load_fen(self, fen: str) -> None:
        rows = fen_utils.make_complete(fen)

        index = 56 
        for row in rows:
            for char in row:
                if char.isdigit():
                    index += int(char)
                else:
                    color, piece = self.bitboard_location_from_piece_name(char)
                    bitboard = self.bitboards[color][piece]
                    self.bitboards[color][piece] = bitwise.set_bit(bitboard, index)
                    index += 1
            index -= 16

    def bitboard_location_from_piece_name(self, name: str) -> int:
        color = WHITE if name.isupper() else BLACK
        if name in "Pp":
            piece = PAWN
        elif name in "Kk":
            piece = KING
        elif name in "Qq":
            piece = QUEEN
        elif name in "Nn":
            piece = KNIGHT
        elif name in "Bb":
            piece = BISHOP
        elif name in "Rr":
            piece = ROOK
        else:
            piece = NULL

        return color, piece 

    def board(self):
        board = 0
        for color, color_boards in self.bitboards.items():
            for piece, piece_board in color_boards.items():
                if piece != NULL:
                    board = board | piece_board
        
        return board
    
    def get_piece_at_index(self, index):
        for color, pieces in self.bitboards.items():
            for piece_type, bitboard in pieces.items():
                if piece_type != NULL:
                    if bitwise.get_bit(bitboard, index):
                        piece_char = self.piece_char(piece_type, color == WHITE)
                        return piece_char
        return '.'

    def piece_char(self, piece_type, is_white):
        piece_symbols = {
            PAWN: 'P',
            KNIGHT: 'N',
            BISHOP: 'B',
            ROOK: 'R',
            QUEEN: 'Q',
            KING: 'K'
        }
        return piece_symbols[piece_type].upper() if is_white else piece_symbols[piece_type].lower()
    
    def piece_type_to_num(self, piece_type: str):
        pieces = {
            'p': PAWN,
            'q': QUEEN,
            'k': KING,
            'r': ROOK,
            'b': BISHOP,
            'n': KNIGHT
        }

        return pieces[piece_type.lower()]

    def move_piece(self, move: Move):
        from_pos, to_pos = move.from_pos, move.to_pos
        color = BLACK if move.color == COLOR["BLACK"] else WHITE
        piece_type = self.piece_type_to_num(move.piece_type)

        from_index = from_pos.index
        to_index = to_pos.index

        self.bitboards[color][piece_type] &= ~(1 << from_index)

        opposing_color = WHITE if color == BLACK else BLACK
        captured_piece_type = None
        for p_type in self.bitboards[opposing_color]:
            if self.bitboards[opposing_color][p_type] & (1 << to_index):
                self.bitboards[opposing_color][p_type] &= ~(1 << to_index)
                captured_piece_type = p_type
                break

        self.bitboards[color][piece_type] |= (1 << to_index)

        # TODO Additional checks (castling, pawn promotion, en passant)


    def show(self):
        board_binary = f"{self.board():064b}"
        print(f"{self.board()} -> {board_binary}")

        board_binary = board_binary[::-1]

        rows = [board_binary[i:i+8] for i in range(0, len(board_binary), 8)][::-1]

        print("  +-----------------+")
        for rank in range(8):
            print(f"{8 - rank} |", end=' ')
            for file in range(8):
                index = (7 - rank) * 8 + file 
                piece = self.get_piece_at_index(index)
                print(piece, end=' ')
            print("|")
        print("  +-----------------+")
        print("    a b c d e f g h ")


        
                    
            
                                

