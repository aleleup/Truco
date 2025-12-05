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

# class TestWebSocket(BaseModel):
#     id: int
# app = FastAPI()
# Response = dict[str, str]
# @app.get("/")
# def read_root() -> Response:
#     return {"message": "Hello World"}

# @app.get("/new-endpoint")
# def new_endpoint() -> Response:
#     return {"message": "NEW ENDPOINT"}

# # desk = GameDesk()

# @app.get("/new_row")
# def show_cards():
#     return desk.init_row()

# @app.get("/status")
# def show_players_status():
#     return desk.players_status()

# @app.post("/players_action")
# def player_throws_card(body: PlayerActionModel):
#    if type(body.action["card_index"]) == int and type(body.action["bet"]) == list:
#         new_action = PlayersActions(body.action["card_index"], body.action["bet"])
#         return desk.receive_players_action(body.id, new_action)
    

# @app.get("/player/{id}")
# def player_by_id(id: int):
#     return desk.show_player_data_by_id(id)

# @app.get("/desk-status")
# def desk_status():
#     return desk.see_desk_status()


# @app.websocket("/ws")
# async def websocket_endpoint(ws: WebSocket):
#     await ws.accept()
#     await ws.send_json({"event": "welcome"})



############# AUX-FUNCTIONS #############
async def send_players_status(game_desk:GameDesk, connection_manager: ConnectionManager):
    for id in [0,1]: 
            status: PlayerStatus = game_desk.player_status(id)
            print("PLAYER_STATUS", status)
            await connection_manager.send_to(id, json.dumps(status))


####### USAGE OF WEB-SOCKETS #######
if __name__ == "main":

    app = FastAPI()
    test_manager = ConnectionManager(2)

    @app.websocket("/ws/{client_id}")
    async def websocket_endpoint(websocket: WebSocket, client_id: int):
        await test_manager.connect(client_id, websocket)

        try:
            while True:
                data = await websocket.receive_text()
                # data: {"to": int, "from": int, "payload": data}
                await handle_message(client_id, data)

        except WebSocketDisconnect:
            await test_manager.disconnect(client_id)

    async def handle_message(sender_id: int, raw_data: str):
        print("Pre-parsing data: ", sender_id, raw_data)
        data = json.loads(raw_data)

        target_id = data["to"]
        payload = data["payload"]

        # ✅ PROCESS LOGIC (game rules, validation, etc.)
        result = f"Processed '{payload}' from {sender_id}"

        # ✅ SEND RESULT TO TARGET CLIENT
        await test_manager.send_to(target_id, result)
        # Send "respond" to sender
        await test_manager.send_to(sender_id, "Message send and read correctly")


    ### KEEP CLIENTS IN LOBBY UNTIL TWO PLAYERS ARE CONNECTED (There's no need to use databases for this logic now)
    host: ConnectionManager = ConnectionManager(2)
    @app.websocket("/enter-lobby/{id}")
    async def receive_player(websocket: WebSocket, id:str):
        new_id: int = 1 if host.connections_amount() > 0 else 0
        await host.connect(new_id, websocket) # send them into the lobby and return their new id
        await host.send_to(new_id, json.dumps({"new_id": new_id}))
        
        try:
            if host.connections_amount() == 2:
                    message: dict[str, bool] = {"allow_access": True} 
                    await host.broadcast(json.dumps(message))
                    await host.shutdown()
                    return
            while True:
                if websocket.client_state.name == "CONNECTED":
                    await websocket.receive_text()
                
        except WebSocketDisconnect:
            await host.disconnect(new_id)
    
    desk: GameDesk = GameDesk()
    players_middleware: ConnectionManager = ConnectionManager(2)
    @app.websocket("/playground/{id}")
    async def start_game(websocket: WebSocket, id: int):
        await players_middleware.connect(id, websocket)
        if players_middleware.connections_amount() == 2:
            desk.init_row()
            await send_players_status(desk, players_middleware)
        try:
            while True:  # keep this socket alive forever
                raw = await websocket.receive_text()

                player_action: ActionPayload = json.loads(raw)
                card_index: int = player_action["card_index"]
                bet: list[str] = player_action["bet"]

                new_action = PlayersActions(card_index, bet)
                desk.receive_players_action(id, new_action)
                await send_players_status(desk, players_middleware)
        
        except WebSocketDisconnect:
            await players_middleware.disconnect(id)


