import engine.utils as utils 
from pprint import pprint 

def test_fen_to_attributes():
    bb = utils.fen_to_bitboards('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    pprint(bb)