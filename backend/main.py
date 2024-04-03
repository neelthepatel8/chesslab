from fastapi import FastAPI, WebSocket
import json
from engine import *
from constants import *
from engine import fen_utils
from engine.constants import *

app = FastAPI()
board = None

@app.get("/")
async def root():
    return {"message": "Chess Game Backend Running"}


async def init_board(websocket, message):
    global board

    board = Board()
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
                "NO_MOVE_MADE": NO_MOVE_MADE,
                "MOVE_MADE": MOVE_MADE,
                "NO_KILL": NO_KILL,
                "KILL": KILL,
                "CHECK": CHECK,
                "NO_CHECK": NO_CHECK,
                "CHECKMATE": CHECKMATE,
                "STALEMATE": STALEMATE,
                "PROMOTE_POSSIBLE": PROMOTE_POSSIBLE,
                "ERR_NO_POSITIONS": ERR_NO_POSITIONS,
                "ERR_NO_PIECE": ERR_NO_PIECE,
                "ERR_ILLEGAL_MOVE": ERR_ILLEGAL_MOVE,
                "PROMOTED": PROMOTED,
                "NOT_PROMOTED": NOT_PROMOTED,
                "CASTLED": CASTLED,
                "CASTLED_CHECK": CASTLED_CHECK,
                "CASTLED_NO_CHECK": CASTLED_NO_CHECK,
                'ERROR_NO_POSITIONS_PROVIDED':ERROR_NO_POSITIONS_PROVIDED, 
                'ERROR_NO_PIECE_TO_MOVE': ERROR_NO_PIECE_TO_MOVE,
                'ERROR_MOVE_NOT_POSSIBLE': ERROR_MOVE_NOT_POSSIBLE,
                'SUCCESS_MOVE_MADE_NO_KILL_NO_CHECK': SUCCESS_MOVE_MADE_NO_KILL_NO_CHECK,
                'SUCCESS_MOVE_MADE_NO_KILL_CHECK': SUCCESS_MOVE_MADE_NO_KILL_CHECK,
                'SUCCESS_MOVE_MADE_WITH_KILL_NO_CHECK': SUCCESS_MOVE_MADE_WITH_KILL_NO_CHECK,
                'SUCCESS_MOVE_MADE_WITH_KILL_NO_CHECK': SUCCESS_MOVE_MADE_WITH_KILL_NO_CHECK,
                'SUCCESS_MOVE_MADE_WITH_KILL_CHECK': SUCCESS_MOVE_MADE_WITH_KILL_CHECK,
                "SUCCESS_MOVE_MADE_NO_KILL_CHECKMATE": SUCCESS_MOVE_MADE_NO_KILL_CHECKMATE,
                "SUCCESS_MOVE_MADE_NO_KILL_STALEMATE": SUCCESS_MOVE_MADE_NO_KILL_STALEMATE,
                "SUCCESS_MOVE_MADE_WITH_KILL_CHECKMATE": SUCCESS_MOVE_MADE_WITH_KILL_CHECKMATE,
                "SUCCESS_MOVE_MADE_WITH_KILL_STALEMATE": SUCCESS_MOVE_MADE_WITH_KILL_STALEMATE,
                "SUCCESS_MOVE_MADE_WTIH_KILL_PROMOTE_POSSIBLE": SUCCESS_MOVE_MADE_WTIH_KILL_PROMOTE_POSSIBLE,
                "SUCCESS_MOVE_MADE_NO_KILL_PROMOTE_POSSIBLE": SUCCESS_MOVE_MADE_NO_KILL_PROMOTE_POSSIBLE,
                "SUCCESS_PAWN_PROMOTED_CHECKMATE": SUCCESS_PAWN_PROMOTED_CHECKMATE,
                "SUCCESS_PAWN_PROMOTED_STALEMATE": SUCCESS_PAWN_PROMOTED_STALEMATE,
                "SUCCESS_PAWN_PROMOTED_CHECK": SUCCESS_PAWN_PROMOTED_CHECK,
                "SUCCESS_MOVE_MADE_NO_KILL_NO_CHECK_CASTLED": SUCCESS_MOVE_MADE_NO_KILL_NO_CHECK_CASTLED,
                "SUCCESS_MOVE_MADE_NO_KILL_CHECK_CASTLED": SUCCESS_MOVE_MADE_NO_KILL_CHECK_CASTLED,
            }
        },
    }
    await websocket.send_text(json.dumps(response))
    

async def possible_moves(websocket, message):
    global board

    if "data" not in message: await websocket.send_text(json.dumps(RESPONSE_ERROR_DATA))
    if "position" not in message["data"]: await websocket.send_text(json.dumps(RESPONSE_ERROR_POSITION))

    position = message['data']['position']
    possible_moves = board.get_legal_moves(position)
    chess_notation_moves = fen_utils.convert_coords_to_chess_notation(possible_moves)
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

    if "data" not in message: await websocket.send_text(json.dumps(RESPONSE_ERROR_DATA))
    if "from_position" not in message["data"]: await websocket.send_text(json.dumps(RESPONSE_ERROR_POSITION))
    if "to_position" not in message["data"]: await websocket.send_text(json.dumps(RESPONSE_ERROR_POSITION))

    from_pos = message['data']['from_position']
    to_pos = message['data']['to_position']

    move_success, is_kill, special = board.move_piece(from_pos, to_pos)

    response = {
        'type': 'move_piece',
        'data': {
            'fen': board.make_fen(),
            'move_success': move_success,
            'is_kill': is_kill,
            'special': special
        },

        'error': special,
    }

    await websocket.send_text(json.dumps(response))

async def promote_pawn(websocket, message):
    global board

    if "data" not in message: await websocket.send_text(json.dumps(RESPONSE_ERROR_DATA))
    if "position" not in message["data"]: await websocket.send_text(json.dumps(RESPONSE_ERROR_POSITION))
    if "promote_to" not in message["data"]: await websocket.send_text(json.dumps(RESPONSE_ERROR_PROMOTE_TYPE))

    position = message['data']['position']
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

message_handlers = {
    'init': init_board,
    'configuration': configuration,
    'poss_moves': possible_moves,
    'move_piece': make_move,
    'promote_pawn': promote_pawn,
}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        message = json.loads(data)
        handler = message_handlers.get(message["type"])
        if handler:
            await handler(websocket, message)
        else:
            print(f"Unknown message type: {message['type']}")


