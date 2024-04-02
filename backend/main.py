from fastapi import FastAPI, WebSocket
import json
from engine import *
from constants import *
from engine import fen_utils

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

    move_success, is_kill, error = board.move_piece(from_pos, to_pos)

    response = {
        'type': 'move_piece',
        'data': {
            'fen': board.make_fen(),
            'move_success': move_success,
            'is_kill': is_kill,
        },

        'error': error,
    }

    await websocket.send_text(json.dumps(response))




message_handlers = {
    'init': init_board,
    'poss_moves': possible_moves,
    'move_piece': make_move,
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


