from engine.constants import COLOR, MAX_RANK, MAX_FILE
import engine.pieces as pieces
from engine.Position import Position
from engine.player.BlackPlayer import BlackPlayer
from engine.player.WhitePlayer import WhitePlayer

def build_board_from_fen(fen):
    board = [[None for _ in range(MAX_FILE)] for _ in range(MAX_RANK)]
    complete_fen = make_complete(fen)
    for rank in range(MAX_RANK):
        for file in range(MAX_FILE):
            piece = get_piece_from_char(complete_fen[rank][file], rank + 1, file + 1)
            board[rank][file] = piece

    return board

def get_piece_from_char(name, rank, file):
    black = COLOR["BLACK"]
    white = COLOR["WHITE"]
    position = Position(rank=rank, file=file)
    piece_map = {
        'p': pieces.Pawn(position, black),
        'q': pieces.Queen(position, black),
        'r': pieces.Rook(position, black),
        'b': pieces.Bishop(position, black),
        'n': pieces.Knight(position, black),
        'k': pieces.King(position, black),
        'P': pieces.Pawn(position, white),
        'Q': pieces.Queen(position, white),
        'R': pieces.Rook(position, white),
        'B': pieces.Bishop(position, white),
        'N': pieces.Knight(position, white),
        'K': pieces.King(position, white),
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

def coords_to_algebraic(position: Position):
    num2letter = {
        1: "a",
        2: "b",
        3: "c",
        4: "d",
        5: "e",
        6: "f",
        7: "g",
        8: "h",
    }
    
    new_file = num2letter[position.file]
    return f"{new_file}{8 + 1 - position.rank}"

def get_current_player(fen):
    if not fen: 
        return WhitePlayer()

    _, turn, _, _, _, _ = fen.split(" ")
    return WhitePlayer() if turn == "w" else BlackPlayer()

def get_halfmoves(fen):
    if not fen: 
        return COLOR["WHITE"]

    _, _, _, _, halfmoves, _ = fen.split(" ")
    return int(halfmoves)

def get_fullmoves(fen):
    if not fen: 
        return COLOR["WHITE"]

    _, _, _, _, _, fullmoves = fen.split(" ")
    return int(fullmoves)

def get_castling_availability(fen):
    if not fen: 
        return COLOR["WHITE"]

    _, _, castling_availability, _, _, _ = fen.split(" ")
    return set([letter for letter in castling_availability])


def get_opposite_player(player):
    return COLOR["BLACK"] if player == COLOR["WHITE"] else COLOR["WHITE"]


def algebraic_list(arr: list):
    return [coords_to_algebraic(position) for position in arr]

def algebraic_list_to_coords(arr):
    coords_list = []
    for each in arr:
        if isinstance(each, list):
            sublist = []
            for pos in each:
                alg = algebraic_to_coords(pos)
                sublist.append(alg)
            coords_list.append(sublist)
        else:
            alg = algebraic_to_coords(each)
            coords_list.append(each)
    return coords_list


def algebraic_list_to_positions(algebraic_lists):
    position_lists = []
    for algebraic_list in algebraic_lists:
        position_list = [Position(algebraic=algebraic) for algebraic in algebraic_list]
        position_lists.append(position_list)
    return position_lists
