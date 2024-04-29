from engine.FastBoard.FastBoard import FastBoard
from engine.player import Player, BlackPlayer, WhitePlayer
import engine.MoveGen as MoveGen
from engine.MoveGen.magic import ROOK_MAGICS, BISHOP_MAGICS 
from engine.constants import COLOR
from engine.Position import Position
import engine.MoveGen.setup as setup
from queue import PriorityQueue
from collections import namedtuple

Move = namedtuple('Move', ('start', 'end', 'pieceType', 'color', 'captureType',
                           'captureStrength', 'isPrincipleVariation'))

class MovePQ(PriorityQueue):
    def __init__(self):
        super().__init__()
        self.size = 0

    def push(self, move):
        if move.isPrincipleVariation:  priority = 0
        elif move.captureType is None: priority = 6
        elif move.captureStrength < 0: priority = 7
        else:                          priority = 5-move.captureStrength

        self.put((priority,move))
        self.size += 1

    def clear(self):
        self.size = 0
        super().clear()

    def pop(self):
        self.size -= 1
        priority,move = self.get()
        return move

    def __len__(self):
        return self.size
    
    def __str__(self):
        temp_list = []
        while not self.empty():
            temp_list.append(self.get())

        result = ""
        for priority, move in temp_list:
            result += f"{move.start} -> {move.end}, "
            self.put((priority, move))

        return result


class Generator:
    def __init__(self):
        self.masks = setup.load_move_masks()
        self.moves, self.movesets = setup.Moves, setup.MoveSets
        self.bishopMagic, self.rookMagic = setup.load_magic()
        self.principleVariations = {}
        
        
    def find_attacks(self, board: FastBoard): 
        attacks = [], []
        attackSets = [0] * 2

        for piece, pieceType, color in board.pieces:

            if pieceType == 0:
                pieceAttacks = self.movesets[pieceType][color][piece][1]

            elif pieceType == 5 or pieceType == 1:
                pieceAttacks = self.movesets[pieceType][piece]

            elif pieceType == 2 or pieceType == 3:
                args = (piece, pieceType, board.occupied)
                pieceAttacks = self.search_magic_cache(*args)

            elif pieceType == 4:
                straights = self.search_magic_cache(piece, 2, board.occupied)
                diagonals = self.search_magic_cache(piece, 3, board.occupied)
                pieceAttacks = straights | diagonals


            attacks[color].append(pieceAttacks)
            attackSets[color] |= pieceAttacks

        return attacks, attackSets

    def search_magic_cache(self, piece, pieceType, occupied):
        magic = self.bishopMagic if pieceType == 2 else self.rookMagic
        blockers = magic.attacks[piece] & occupied
        magicBitboard = magic.bitboards[piece]
        numAttackIndices = magic.indices[piece]
        magicKey = (blockers * magicBitboard) >> (64 - numAttackIndices)
        return magic.cache[piece][magicKey]

    def find_captures(self, board, attacks, attackSets):
        return self.find_moves(board, attacks, attackSets, minCaptureStrength = -6)

    def find_strong_captures(self, board, attacks, attackSets, findTrades=False):
        return self.find_moves(board, attacks, attackSets,
                            minCaptureStrength = 0 if findTrades else 1)

    def find_moves(self, board, attacks, attackSets, minCaptureStrength=None):
        onlyCaptures = minCaptureStrength is not None
        moves = MovePQ()

        color = board.active
        friends = board.colors[color]
        enemies = board.colors[not color]
        threatened = attackSets[not color]

        pieceIndex = 0
        for piece, pieceType in board.pieces.get_color(color):
            pieceAttacks = attacks[color][pieceIndex]
            pieceIndex+=1

            if pieceType == 0:
                moveset,attackSet = self.movesets[0][color][piece]

                blocker = self.masks.pawnBlockers[color][piece]

                pawnIsBlocked = blocker & board.occupied != 0

                if pawnIsBlocked:
                    moveMask = 0
                else:
                    moveMask = moveset & ~board.occupied

                attackMask = attackSet & enemies

                legalMoveMask = attackMask | moveMask

            elif pieceType == 5:
                legalMoveMask = pieceAttacks & ~friends & ~threatened

            else:
                legalMoveMask = pieceAttacks & ~friends

            if pieceType == 0:
                cachedMoves = self.moves[pieceType][color][piece]
            else:
                cachedMoves = self.moves[pieceType][piece]

            for moveBitboard in cachedMoves:
                if moveBitboard & legalMoveMask != 0:
                    isACapture = moveBitboard & enemies != 0
                    if isACapture:
                        captureType = board.get_piece_type(moveBitboard)

                        get_piece_rank = lambda pt: pt - 1 if pt >= 2 else pt

                        captureStrength = get_piece_rank(captureType) \
                                        - get_piece_rank(pieceType)

                        move = Move(piece, moveBitboard, pieceType, color,
                                    captureType, captureStrength, False)
                    else:
                        move = Move(piece, moveBitboard, pieceType,
                                    color, None, None, False)


                    if onlyCaptures and (move.captureType is None
                        or minCaptureStrength > move.captureStrength): continue

                    moves.push(move)


        return moves

    def set_a_principle_variation(self, board, move):
        self.principleVariations[board] = move