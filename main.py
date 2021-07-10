# 3rd party
from fastapi import FastAPI
from fastapi import WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.websockets import WebSocketDisconnect
from fastapi.responses import Response

# Local
from database.ctl import database
from database.ctl import targets
from database.models import Target
from language import PING_NOT_REACHABLE
from language import PING_REACHABLE
from utils import ping
import sqlite3
from awake.wol import send_magic_packet

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        ip = await websocket.receive_text()
        while True:
            await websocket.receive_text()
            await websocket.send_text(PING_REACHABLE if ping(ip) else PING_NOT_REACHABLE)
    except WebSocketDisconnect:
        pass


@app.post("/send-wol")
async def send_wol(target: Target):
    send_magic_packet(mac=target.mac, broadcast=target.broadcast, dest=target.ip, port=9)
    send_magic_packet(mac=target.mac, broadcast=target.broadcast, dest=target.ip, port=7)
    return ""


@app.get("/target")
async def get_all_targets():
    query = targets.select()
    return await database.fetch_all(query)


@app.post("/target")
async def add_new_target(item: Target):
    query = targets.insert().values(**item.dict())
    try:
        await database.execute(query)
    except sqlite3.IntegrityError as e:
        return Response(str(e), status_code=400)
    return {**item.dict()}


@app.delete("/target")
async def remove_target(mac: str) -> str:
    query = targets.delete().where(targets.columns.mac == mac)
    await database.execute(query)
    return mac
