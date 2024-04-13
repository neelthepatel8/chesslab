import chess.pgn
from engine.Move import Move
from engine.Position import Position
import requests
from engine.Game import Game

import os

directory = 'pgn/game_data'
if not os.path.exists(directory):
    os.makedirs(directory)

class PGNParser:
    def __init__(self, pgn_url):
        self.pgn_file = self.open_file_from_url(pgn_url)
        self.tags = {}
        self.moves = []
        self.comments = []  
        self.game = Game()
        
    def open_file_from_url(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            file_name = f"pgn/game_data/{url.split('/')[-1]}.pgn"
            pgn_file = open(file_name, 'w')
            pgn_file.write(response.text)
            pgn_file.close()
            return file_name
        

    def parse(self):
        pgn_file = open(self.pgn_file, "r")
        pgn = chess.pgn.read_game(pgn_file)
        self.extract_tags(pgn)
        self.extract_moves(pgn)
        pgn_file.close()
        
        self.game.set_moves(self.moves)
        return self.game

    def extract_tags(self, pgn):
        self.tags = dict(pgn.headers)

    def extract_moves(self, pgn):
        node = pgn
        while node.variations:
            next_node = node.variation(0)
            move = next_node.move
            piece_type = node.board().piece_at(move.from_square)
            if piece_type:
                piece_symbol = piece_type.symbol().upper() if piece_type.color == chess.WHITE else piece_type.symbol().lower()
            else:
                piece_symbol = None 

            from_pos = Position(algebraic=chess.square_name(move.from_square))
            to_pos = Position(algebraic=chess.square_name(move.to_square))
            self.moves.append(Move(from_pos, to_pos, piece_symbol))
            node = next_node
