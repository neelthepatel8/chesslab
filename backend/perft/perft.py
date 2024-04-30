from valkyrie.Valkyrie import Valkyrie 
from engine.FastBoard.FastBoard import FastBoard 
from engine.MoveGen.Generator import Generator 
from engine.bitmanipulation.utils import lsb
from engine.Position import Position


def present_move(move):
    start = Position(index=lsb(move.start))
    end = Position(index=lsb(move.end)) 
    
    return f"{start}{end}"
    

def init():
    global generator, board 
    board = FastBoard()
    generator = Generator()
    
def perft(depth, divide=4):
    global generator, board
    nodes = 0
    captures = 0

    if depth == 0:
        return 1, 0
    
    attacks, attackSets = generator.find_attacks(board)
    moves = generator.find_moves(board, attacks, attackSets)
    
    if divide == depth:
        while len(moves) > 0:
            move = moves.pop()
            board += move
            count, _ = perft(depth - 1) 
            board -= move
            print(f"Move {present_move(move)}: {count}")
            nodes += count
            captures += 1 if move.captureType is not None else 0
    else:
        while len(moves) > 0:
            move = moves.pop()
            board += move
            nodes += perft(depth - 1)[0]
            board -= move

    return nodes, captures


def test_perft():
    init()
    for i in range(3, 4):
        
        nodes, captures = perft(i, divide=i)
        print(f"Depth {i} | Nodes Searched: {nodes} | Captures: {captures}")
        
    