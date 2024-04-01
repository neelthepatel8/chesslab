from constants import *
from piece import Piece
from pieces import *

def build_board_from_fen(fen):
    board = [[None for _ in range(MAX_COLS)] for _ in range(MAX_ROWS)]

    placements, active_color, castling, en_passant, halfmove, fullmove = fen.split(' ')

    rows = placements.split('/')

    complete_fen = make_complete(fen)
    for rank in range(MAX_ROWS):
        for file in range(MAX_COLS):
            piece = get_piece_from_char(complete_fen[rank][file], rank + 1, file + 1)
            board[rank][file] = piece

    return board

def get_piece_from_char(name, rank, file):
    black = COLOR["BLACK"]
    white = COLOR["WHITE"]
    piece_map = {
        'p': Pawn(rank, file, black),
        'q': Queen(rank, file, black),
        'r': Rook(rank, file, black),
        'b': Bishop(rank, file, black),
        'n': Knight(rank, file, black),
        'k': King(rank, file, black),
        'P': Pawn(rank, file, white),
        'Q': Queen(rank, file, white),
        'R': Rook(rank, file, white),
        'B': Bishop(rank, file, white),
        'N': Knight(rank, file, white),
        'K': King(rank, file, white),
        'X': None
    }

    return piece_map[name]

def make_complete(fen):
    possible_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    complete_fen = []
    for row in fen.split(' ')[0].split('/'):
        for num in possible_numbers:
            if str(num) in row:
                row = row.replace(str(num), "X" * num)
        complete_fen.append(row)

    return complete_fen


def make_compact(fen):
    compact_fen_rows = []

    for row in fen.split(' ')[0].split('/'):
        compact_row = ""
        count = 0
        for char in row:
            if char == "X":
                count += 1
            else:
                if count > 0:
                    compact_row += str(count)
                    count = 0
                compact_row += char
        if count > 0:
            compact_row += str(count)

        compact_fen_rows.append(compact_row)

    return '/'.join(compact_fen_rows)


def algebraic_to_coords(algebraic_notation):
    file_to_num = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}

    file_letter = algebraic_notation[0]
    rank_number = 9 - int(algebraic_notation[1])

    file_number = file_to_num[file_letter]

    return (rank_number, file_number)
