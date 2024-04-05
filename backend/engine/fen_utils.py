from engine.constants import COLOR, MAX_RANK, MAX_FILE
import engine.pieces as pieces

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
    piece_map = {
        'p': pieces.Pawn(rank, file, black),
        'q': pieces.Queen(rank, file, black),
        'r': pieces.Rook(rank, file, black),
        'b': pieces.Bishop(rank, file, black),
        'n': pieces.Knight(rank, file, black),
        'k': pieces.King(rank, file, black),
        'P': pieces.Pawn(rank, file, white),
        'Q': pieces.Queen(rank, file, white),
        'R': pieces.Rook(rank, file, white),
        'B': pieces.Bishop(rank, file, white),
        'N': pieces.Knight(rank, file, white),
        'K': pieces.King(rank, file, white),
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

def coords_to_algebraic(rank, file):
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
    new_file = num2letter[file]
    return f"{new_file}{8 + 1 - rank}"


def convert_coords_to_chess_notation(possible_moves):
    converted_moves = []

    if not possible_moves: 
        return []
    for move in possible_moves:
        rank, file = move
        converted_moves.append(coords_to_algebraic(rank, file))

    return converted_moves

def get_current_player(fen):
    if not fen: 
        return COLOR["WHITE"]

    _, turn, _, _, _, _ = fen.split(" ")
    return COLOR["WHITE"] if turn == "w" else COLOR["BLACK"]

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


def algebraic_list(arr):
    return [coords_to_algebraic(r, f) for r, f in arr]