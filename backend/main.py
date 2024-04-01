from fastapi import FastAPI, WebSocket
import json

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Chess Game Backend Running"}


async def init_board(websocket, message):
    start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    message = {
        'type': 'init',
        'data': {
            'fen': start_fen
        },
        'error': None,
    }
    await websocket.send_text(json.dumps(message))

message_handlers = {
    'init': init_board,
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
