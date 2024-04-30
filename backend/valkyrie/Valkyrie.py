from engine.FastBoard.FastBoard import FastBoard
from engine.MoveGen.Generator import Generator
import time
from valkyrie.Valkulator import Valkulator
from pprint import pprint
from engine.Position import Position
from engine.bitmanipulation.utils import lsb



class Valkyrie():
    def __init__(self):
        self.generator = Generator()
        self.evaluator = Valkulator()
    
    def best_move(self, board: FastBoard):
        alpha, beta = -1000, 1000
        maximizeRoot = not board.active 
        depth, maxDepth = 0, 5

        evaluation, best_move = self.search(board, maximizeRoot, alpha, beta, depth, maxDepth, 1000)
        
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

        if len(moves) == 0:
            if depth < maxDepth:
                return -1000 if maximize else 1000, None
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
        
        # def present_move(move):
        #     start = Position(index=lsb(move.start))
        #     end = Position(index=lsb(move.end)) 
            
        #     return f"{start}{end}"
        # print("Looking for best move for: ", maximize)
        # pprint([(present_move(b), a) for (a, b) in moveOrder])
        
        
        # return

        # beam search
        if depth == maxDepth - 1: 
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
            if maximize == 0:
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
            
            