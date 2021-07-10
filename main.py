# 3rd party
from fastapi import FastAPI
from fastapi import WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.websockets import WebSocketDisconnect

# Local
from language import PING_NOT_REACHABLE
from language import PING_REACHABLE
from utils import ping

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        ip = await websocket.receive_text()
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(PING_REACHABLE if ping(ip) else PING_NOT_REACHABLE)
    except WebSocketDisconnect:
        pass
