import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from classes.GameDesk import GameDesk
from classes.PlayersActions import PlayersActions
from classes.ConnectionManager import ConnectionManager
from constants.types import *
from pydantic import BaseModel
class PlayerActionModel(BaseModel):
    id: int
    action: dict[str, int | list[str]]
class TestWebSocket(BaseModel):
    id: int
app = FastAPI()
Response = dict[str, str]
@app.get("/")
def read_root() -> Response:
    return {"message": "Hello World"}

@app.get("/new-endpoint")
def new_endpoint() -> Response:
    return {"message": "NEW ENDPOINT"}

desk = GameDesk()

@app.get("/new_row")
def show_cards():
    return desk.init_row()

@app.get("/status")
def show_players_status():
    return desk.players_status()

@app.post("/players_action")
def player_throws_card(body: PlayerActionModel):
   if type(body.action["card_index"]) == int and type(body.action["bet"]) == list:
        new_action = PlayersActions(body.action["card_index"], body.action["bet"])
        return desk.receive_players_action(body.id, new_action)
    

@app.get("/player/{id}")
def player_by_id(id: int):
    return desk.show_player_data_by_id(id)

@app.get("/desk-status")
def desk_status():
    return desk.see_desk_status()


# @app.websocket("/ws")
# async def websocket_endpoint(ws: WebSocket):
#     await ws.accept()
#     await ws.send_json({"event": "welcome"})







####### USAGE OF WEB-SOCKETS #######
if __name__ == "main":

    app = FastAPI()
    manager = ConnectionManager()

    @app.websocket("/ws/{client_id}")
    async def websocket_endpoint(websocket: WebSocket, client_id: int):
        await manager.connect(client_id, websocket)

        try:
            while True:
                data = await websocket.receive_text()
                # data: {"to": int, "from": int, "payload": data}
                await handle_message(client_id, data)

        except WebSocketDisconnect:
            manager.disconnect(client_id)

    async def handle_message(sender_id: int, raw_data: str):
        print("Pre-parsing data: ", sender_id, raw_data)
        data = json.loads(raw_data)

        target_id = data["to"]
        payload = data["payload"]

        # ✅ PROCESS LOGIC (game rules, validation, etc.)
        result = f"Processed '{payload}' from {sender_id}"

        # ✅ SEND RESULT TO TARGET CLIENT
        await manager.send_to(target_id, result)
        # Send "respond" to sender
        await manager.send_to(sender_id, "Message send and read correctly")