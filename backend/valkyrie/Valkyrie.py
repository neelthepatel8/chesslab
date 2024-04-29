from engine.board import Board
import engine.constants as constants
from engine.player.Player import Player
from engine.piece import Piece
from graphviz import Digraph
from engine.FastBoard.FastBoard import FastBoard
from engine.MoveGen.Generator import Generator
import time
from valkyrie.Valkulator import Valkulator



class Valkyrie():
    def __init__(self):
        self.generator = Generator()
        self.evaluator = Valkulator()
    
    # def get_all_moves(self, board: Board, player: Player) -> list[Move]:
    #     return board.get_all_legal_moves_with_origin(player)
        
    # def evaluate(self, board: Board):
    #     black_score, white_score = 0, 0
    #     for row in board.board:
    #         for piece in row:
    #             if piece is not None:
    #                 piece_value = self.get_piece_value(piece)
    #                 if piece.get_color() == constants.COLOR["BLACK"]:
    #                     black_score += piece_value
    #                 else:
    #                     white_score += piece_value
            
    #     score = white_score - black_score
        
    #     return score
    
    # def get_piece_value(self, piece: Piece) -> int:
    #     return piece.value + self.get_positional_value(piece)
    
    # def get_positional_value(self, piece: Piece) -> int:
    #     position = piece.position
    #     rank, file = position.coords
    #     position_value = piece.positional_values[rank - 1][file - 1]
    #     return position_value
    
    # def best_move(self, board: Board):                                
    #     dot = Digraph(format='png') 

    #     player = board.current_player
    #     moves = self.get_all_moves(board, player)

    #     initial_board_copy = board.deep_copy()
    #     current_score = self.evaluate(initial_board_copy)
    #     best_score, best_move = current_score, None

    #     root_id = str(initial_board_copy) 
    #     initial_board_board = initial_board_copy.print_board()
    #     dot.node(root_id, label=f'Initial Score: {current_score}\n{initial_board_board}')

    #     for move in moves:
    #         board_copy = board.deep_copy()
    #         board_copy.move(move.from_pos, move.to_pos)
    #         new_score = self.evaluate(board_copy)
            
    #         is_better_move = new_score >= best_score if player == constants.COLOR["WHITE"] else new_score <= best_score
    #         if is_better_move:
    #             best_score = new_score
    #             best_move = move
            
    #         # Update graph:
    #         move_id = str(board_copy)  
    #         board_board = board_copy.print_board()
    #         dot.node(move_id, label=f'Move: {move}\nScore: {new_score}\n{board_board}')
    #         dot.edge(root_id, move_id, label=str(move))

    #     dot.render('output/move_tree', view=False) 
    #     return best_move
    
    def best_move(self, board: FastBoard):
        alpha, beta = -1000, 1000
        maximizeRoot = not board.active 
        depth, maxDepth = 0, 5

        evaluation, best_move = self.search(board, maximizeRoot, alpha, beta, depth, maxDepth, 1000)
        print('leaf eval: ' + str(evaluation))
        return best_move
        
    def search(self, board, maximize, alpha, beta, depth, maxDepth, maxValue, isQuiet=True):
        attacks, attackSets = self.generator.find_attacks(board)

        # Recursive base case. Leaf has been reached. Return its valuation.
        if depth >= maxDepth and isQuiet:
            return self.evaluator(board, attacks)

        # only search captures if depth surpassed max depth. If the max depth
        # is surpassed and it's quiet, search all moves, but use stop search
        # parameter to make it the last search on this branch
        if depth < maxDepth:
            moves = self.generator.find_moves(board, attacks, attackSets)
        elif depth == maxDepth:
            moves = self.generator.find_captures(board, attacks, attackSets)
        else:
            moves = self.generator.find_strong_captures(board, attacks, attackSets,
                                                findTrades = depth == maxDepth + 1)

        print(f"All moves found: {moves}")
        return

        if len(moves) == 0:
            assert depth >= maxDepth
            return self.evaluator(board, attacks)
        
        # sorting moves everytime seems to speed things up
        moveOrder = []
        while len(moves) > 0:
            m = moves.pop()
            board+=m
            v = self.evaluator(board,attacks, mode=0)
            moveOrder.append((v,m))
            board -= m
        moves = sorted(moveOrder, key=lambda x:x[0], reverse = board.active == 1)
        moves = [m[1] for m in moves]

        # beam search
        if depth == maxDepth-1: 
            moves = moves[-10:]

        # initilize best as worst value
        best = -maxValue if maximize else maxValue
        bestMove = None

        # search edges until alpha/beta cutoff occurs
        while beta > alpha and len(moves) > 0:

            # get the highest priority move from the move queue
            move = moves.pop()

            # get child node by updating board
            board += move

            # make recursive call to perform depth first search
            value = self.search(board, not maximize, alpha, beta, depth + 1, maxDepth, maxValue, isQuiet = move.captureType is None)
            
            # revert board
            board -= move

            # maximize white and minimize black
            if maximize:
                best = max(value, best)
                alpha = max(alpha, best)
                bestMove = move
            else:
                best = min(value, best)
                beta = min(beta,best)
                bestMove = move

        # if depth is 0, the search is complete
        return (best, bestMove) if depth == 0 else best
    
    def play_computer_game(self):
        MAX_MOVES = 35

        board = FastBoard()

        print(board)
        
        movesMade = 0
        while movesMade < MAX_MOVES:
            movesMade += 1
            
            print(f"Searching for best move for player {'white' if not board.active else 'black'}")
            
            start = time.time()
            best_move = self.best_move(board)
            end = time.time()
            
            board += best_move
            
            print('Found move in ' + str(end - start) + ' seconds')

            scores = self.evaluator.get_scores(1)
            
            attacks, attacksets = self.generator.find_attacks(board)
            
            for label, score, w in zip(['material','pst','center control', 'development', 'tempo', 'connectivity'],scores, self.evaluator.weights):
                print('\t',label,': ', score(board, attacks) * w)

            valuation = self.evaluator(board, self.generator.find_attacks(board)[0])
            print('valuation: ' + str(valuation))
            print(board)
