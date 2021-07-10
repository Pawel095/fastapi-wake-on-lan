from starlette.websockets import WebSocketDisconnect
from language import PING_NOT_REACHABLE, PING_REACHABLE
from fastapi import FastAPI, WebSocket
from utils import ping

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        ip = await websocket.receive_text()
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(
                PING_REACHABLE if ping(ip) else PING_NOT_REACHABLE
            )
    except WebSocketDisconnect:
        pass
