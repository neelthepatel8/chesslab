import chess.pgn
from engine.Move import Move
from engine.Position import Position
import requests
from engine.Game import Game
import random

import os

directory = 'pgn/game_data'
if not os.path.exists(directory):
    os.makedirs(directory)

class PGNParser:
    def __init__(self, file_name=None, url=None, multi=False):
        if file_name:
            self.pgn_file = file_name
        elif url:
            self.pgn_file = self.open_file_from_url(url)
        self.tags = {}
        self.moves = []
        self.comments = []  
        self.multi = multi
        self.game = Game()
        
    def open_file_from_url(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            file_name = f"pgn/game_data/{url.split('/')[-1]}.pgn"
            pgn_file = open(file_name, 'w')
            pgn_file.write(response.text)
            pgn_file.close()
            return file_name
        

    def parse(self, checkmate=False, stalemate=False):
        if self.multi:
            file_list = self.make_multi_files(self.pgn_file, checkmate=checkmate)
        else: 
            file_list = [self.pgn_file]
        
        all_games = []
        if not stalemate: file_list = random.sample(file_list, 20)
        
        for file in file_list:
            with open(file, "r") as pgn_file:
                while True:
                    pgn = chess.pgn.read_game(pgn_file)
                    if not pgn:
                        break
                    
                    board = pgn.end().board()
                    if stalemate and not board.is_stalemate():
                        continue
                    
                    
                    self.extract_tags(pgn)
                    self.extract_moves(pgn)

                    self.game.set_moves(self.moves)
                    self.game.set_winner(pgn.headers['Result'])
                    self.game.name = file
                    all_games.append(self.game)
                    
                    self.game = Game()
                    self.moves = []
                    self.tags = None

        return all_games[:20]


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
            promotion = None
            if move.promotion:
                promotion_piece_type = chess.Piece(move.promotion, piece_type.color)
                promotion = promotion_piece_type.symbol().upper() if piece_type.color == chess.WHITE else promotion_piece_type.symbol().lower()

            self.moves.append(Move(from_pos, to_pos, piece_symbol, promotion))
            node = next_node
            
    def make_multi_files(self, multi_file_name, checkmate=False):
        file_names = []
        pgns = []
        current_pgn = ""
        
        directory = f'pgn/game_data/{multi_file_name}'
        if not os.path.exists(directory):
            os.makedirs(directory)
            
            
        with open(f"pgn/game_data/{multi_file_name}.pgn", 'r') as f:
            for i, line in enumerate(f):
                line = line.strip()
                if line.startswith("[Event "):
                    event_name = line.split(' ')[1] 
                    event_name = event_name[1:-2].lower()
                    event_name = '_'.join(event_name.split(' '))
                    file_name = f"{directory}/{event_name}_{i}.pgn"
                    file_names.append(file_name)
                    pgns.append(current_pgn)
                    current_pgn = line + "\n"
                    
                else:
                    if line.strip() != " " or line.strip() != "":    
                        current_pgn += line + "\n"
        
        all_files = []
        for pgn, file_name in zip(pgns, file_names):
            if pgn.strip() == "" or pgn.strip() == " ":
                continue
            
            if checkmate:
                if "#" not in pgn:
                    continue 

            with open(f"{file_name}", 'w') as f:
                f.write(pgn.strip())
                all_files.append(file_name)
        
        return all_files
                    
                    
