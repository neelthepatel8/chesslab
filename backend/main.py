from fastapi import FastAPI, WebSocket
import json
from engine import Board
import error_responses
from engine import fen_utils
import engine.constants
from fastapi.middleware.cors import CORSMiddleware
from engine.Position import Position

from valkyrie.Valkyrie import Valkyrie

import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("chess_backend")


app = FastAPI(debug=True)
board = None
valkyrie = None

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
    global board
    board = Board()
    valkyrie = Valkyrie()
    
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
    global board

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

    is_kill, special = board.move_piece(from_pos, to_pos)

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
    global board, valkyrie
    
    if valkyrie is None:
        valkyrie = Valkyrie()

    best_move = valkyrie.best_move(board)
    if not best_move:
        print("Error: Valkyrie could not find the best move!")
        return 
    
    is_kill, special = board.move_piece(best_move.from_pos, best_move.to_pos)

    response = {
        'type': 'move_piece',
        'data': {
            'from_pos': best_move.from_pos.algebraic,
            'to_pos': best_move.to_pos.algebraic,
            'fen': board.make_fen(),
            'move_success': 1,
            'is_kill': is_kill,
            'special': special
            },
    }

    await websocket.send_text(json.dumps(response))

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