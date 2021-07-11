# Builtins
import asyncio
import sqlite3

# 3rd party
from awake.wol import send_magic_packet
from fastapi import FastAPI
from fastapi import WebSocket
from fastapi.responses import RedirectResponse
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.websockets import WebSocketDisconnect

# Local
from database.ctl import database
from database.ctl import targets
from database.models import Target
from language import PING_NOT_REACHABLE
from language import PING_REACHABLE
from utils import ping

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


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
            await websocket.send_json(
                {"text": PING_REACHABLE, "code": 1}
                if ping(ip)
                else {"text": PING_NOT_REACHABLE, "code": 0}
            )
    except WebSocketDisconnect:
        await websocket.close()


@app.get("/", response_class=RedirectResponse)
async def redrect_to_index():
    return "/static/index.html"


@app.post("/send-wol")
async def send_wol(target: Target):
    for _ in range(3):
        send_magic_packet(mac=target.mac, broadcast=target.broadcast, port=9)
        await asyncio.sleep(0.1)
        send_magic_packet(mac=target.mac, broadcast=target.broadcast, port=7)
        await asyncio.sleep(0.2)
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
