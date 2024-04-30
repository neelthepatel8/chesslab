from fastapi import FastAPI, WebSocket
import json
from engine import Board
import error_responses
from engine import fen_utils
import engine.constants
from fastapi.middleware.cors import CORSMiddleware
from engine.Position import Position

from engine.utils import bitboard_move_to_object
from valkyrie.Valkyrie import Valkyrie
from engine.player.WhitePlayer import WhitePlayer

import logging
import time 

from collections import namedtuple

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("chess_backend")

Move = namedtuple('Move', ('start', 'end', 'pieceType', 'color', 'captureType',
                           'captureStrength', 'isPrincipleVariation'))
app = FastAPI(debug=True)
board = None
valkyrie = None
fastboard = None 
in_progress = False

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Chess Game Backend Running"}


async def init_board(websocket, message):
    global board, valkyrie, fastboard
    board = Board()
    valkyrie = Valkyrie()
    fastboard = board.to_fastboard()
    
    response = {
        'type': 'init',
        'data': {
            'fen': board.make_fen()
        },
        'error': None,
    }
    await websocket.send_text(json.dumps(response))
    
async def configuration(websocket, message):
    response = {
        'type': 'configuration',
        'data': {
            'constants': {
                "NO_MOVE_MADE": engine.constants.NO_MOVE_MADE,
                "MOVE_MADE": engine.constants.MOVE_MADE,
                "NO_KILL": engine.constants.NO_KILL,
                "KILL": engine.constants.KILL,
                "CHECK": engine.constants.CHECK,
                "NO_CHECK": engine.constants.NO_CHECK,
                "CHECKMATE": engine.constants.CHECKMATE,
                "STALEMATE": engine.constants.STALEMATE,
                "PROMOTE_POSSIBLE": engine.constants.PROMOTE_POSSIBLE,
                "ERR_NO_POSITIONS": engine.constants.ERR_NO_POSITIONS,
                "ERR_NO_PIECE": engine.constants.ERR_NO_PIECE,
                "ERR_ILLEGAL_MOVE": engine.constants.ERR_ILLEGAL_MOVE,
                "PROMOTED": engine.constants.PROMOTED,
                "NOT_PROMOTED": engine.constants.NOT_PROMOTED,
                "CASTLED": engine.constants.CASTLED,
                "CASTLED_CHECK": engine.constants.CASTLED_CHECK,
                "CASTLED_NO_CHECK": engine.constants.CASTLED_NO_CHECK,
                'ERROR_NO_POSITIONS_PROVIDED': engine.constants.ERROR_NO_POSITIONS_PROVIDED, 
                'ERROR_NO_PIECE_TO_MOVE': engine.constants.ERROR_NO_PIECE_TO_MOVE,
                'ERROR_MOVE_NOT_POSSIBLE': engine.constants.ERROR_MOVE_NOT_POSSIBLE,
            }
        },
    }
    await websocket.send_text(json.dumps(response))
    

async def possible_moves(websocket, message):
    global board

    if "data" not in message: 
        await websocket.send_text(json.dumps(error_responses.RESPONSE_ERROR_DATA))
    if "position" not in message["data"]: 
        await websocket.send_text(json.dumps(error_responses.RESPONSE_ERROR_POSITION))

    position = message['data']['position']
    
    position = Position(algebraic=position)
    possible_moves = board.get_legal_moves(position, log=True)
    chess_notation_moves = fen_utils.algebraic_list(possible_moves)
    response = {
        'type': 'poss_moves',
        'data': {
            'possible_moves': chess_notation_moves
        },
        'error': None,
    }
    await websocket.send_text(json.dumps(response))


async def make_move(websocket, message):
    global board, fastboard

    if "data" not in message: 
        await websocket.send_text(json.dumps(error_responses.RESPONSE_ERROR_DATA))
    if "from_position" not in message["data"]: 
        await websocket.send_text(json.dumps(error_responses.RESPONSE_ERROR_POSITION))
    if "to_position" not in message["data"]: 
        await websocket.send_text(json.dumps(error_responses.RESPONSE_ERROR_POSITION))

    from_pos = message['data']['from_position']
    to_pos = message['data']['to_position']
    
    from_pos = Position(algebraic=from_pos)
    to_pos = Position(algebraic=to_pos)

    move_return = board.move_piece(from_pos, to_pos, detailed_return=True)
    
    if len(move_return) == 3:
        is_kill, special, piece = move_return 
    else: 
        is_kill = -1
        special = move_return if len(move_return) == 1 else move_return[1]
        piece = None
    
    if special >= 0:
        move_start = from_pos.index 
        move_end = to_pos.index 
        
        piece_map = {
            'p': 0,
            'n': 1,
            'b': 2,
            'r': 3,
            'q': 4,
            'k': 5
        }
        
        move = Move((1 << move_start), (1 << move_end), piece_map[piece.get_name().lower()], piece.get_color(), 1 if is_kill == 3 else None, None, None)
        fastboard += move
    
    else: 
        print("Error Making Move ", from_pos, to_pos, move, special)
        return
    
    response = {
        'type': 'move_piece',
        'data': {
            'from_pos': from_pos.algebraic,
            'to_pos': to_pos.algebraic,
            'fen': board.make_fen(),
            'move_success': 1,
            'is_kill': is_kill,
            'special': special
        },

        'error': special,
    }

    await websocket.send_text(json.dumps(response))

async def promote_pawn(websocket, message):
    global board

    if "data" not in message: 
        await websocket.send_text(json.dumps(error_responses.RESPONSE_ERROR_DATA))
    if "position" not in message["data"]: 
        await websocket.send_text(json.dumps(error_responses.RESPONSE_ERROR_POSITION))
    if "promote_to" not in message["data"]: 
        await websocket.send_text(json.dumps(error_responses.RESPONSE_ERROR_PROMOTE_TYPE))

    position = message['data']['position']
    position = Position(algebraic=position)
    promote_to = message['data']['promote_to']

    promoted, special = board.try_pawn_promote(position, promote_to=promote_to, do_it=True)

    response = {
        'type': 'promote_pawn',
        'data': {
            'fen': board.make_fen(),
            'promoted': promoted,
            'special': special
        },
    }

    await websocket.send_text(json.dumps(response))
    
async def next_move(websocket, message):
    global board, valkyrie, fastboard, in_progress

    whole_start = time.time()
    
    start_ = time.time()
    best_move = valkyrie.best_move(fastboard)
    end_ = time.time()
    
    print(f"Best Move search: {end_ - start_}s")
    if not best_move:
        print("Error: Valkyrie could not find the best move!")
        return 
    
    best_move_object = bitboard_move_to_object(best_move)
    
    start = time.time()
    is_kill, special = board.move_piece(best_move_object.from_pos, best_move_object.to_pos)
    end = time.time()
    
    if special >= 0:
        fastboard += best_move
        
    else: 
        print("Error Making Move ", best_move, best_move_object, special)
        return 

    print(f"Board Piece Movement: {end - start}s")

    response = {
        'type': 'move_piece',
        'data': {
            'from_pos': best_move_object.from_pos.algebraic,
            'to_pos': best_move_object.to_pos.algebraic,
            'fen': board.make_fen(),
            'move_success': 1,
            'is_kill': is_kill,
            'special': special
            },
    }

    whole_end = time.time()
    print(f"Total time taken to process a best move: {whole_end - whole_start}")
    await websocket.send_text(json.dumps(response))
    in_progress = False

message_handlers = {
    'init': init_board,
    'configuration': configuration,
    'poss_moves': possible_moves,
    'move_piece': make_move,
    'promote_pawn': promote_pawn,
    'next_move': next_move
}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                if not isinstance(message, dict) or "type" not in message:
                    logger.error("Invalid message format")
                    await websocket.send_text(json.dumps({"error": "Invalid message format"}))
                    continue

                handler = message_handlers.get(message["type"])
                if handler:
                    await handler(websocket, message)
                else:
                    logger.error(f"Unknown message type: {message['type']}")
                    await websocket.send_text(json.dumps({"error": "Unknown message type"}))
            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON {e}", exc_info=True)
                await websocket.send_text(json.dumps({"error": "Error decoding JSON"}))
            except KeyError as e:
                logger.error(f"Missing key in message: {e}", exc_info=True)
                await websocket.send_text(json.dumps({"error": f"Missing key: {e}"}))
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)