import json, asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from classes.GameDesk import GameDesk
from classes.ConnectionManager import ConnectionManager
from constants.types import *
# from classes.TrucoDeck import TrucoDeck
############# AUX-FUNCTIONS #############
async def send_players_status(game_desk:GameDesk, connection_manager: ConnectionManager):
    for id in [0,1]: 
            status: PlayerStatus = game_desk.player_status(id)
            print("DEBUG", status)
            await connection_manager.send_to(id, json.dumps(status))
            await asyncio.sleep(0.2)


####### USAGE OF WEB-SOCKETS #######
if __name__ == "main":

    app = FastAPI()

    ### KEEP CLIENTS IN LOBBY UNTIL TWO PLAYERS ARE CONNECTED (There's no need to use databases for this logic now)
    host: ConnectionManager = ConnectionManager(2)
    @app.websocket("/enter-lobby/{id}")
    async def receive_player(websocket: WebSocket, id:str):
        new_id: int = 1 if host.connections_amount() > 0 else 0
        print("CONNECTION NEW ID", new_id)
        await host.connect(new_id, websocket) # send them into the lobby and return their new id
        await host.send_to(new_id, json.dumps({"new_id": new_id}))
        
        try:
            if host.connections_amount() == 2:
                await host.broadcast(json.dumps({"allow_access": True}))

                # Give the OS time to flush frames --> AI HELP
                await asyncio.sleep(0.2)

                await host.shutdown()
                return
            while True:
                if websocket.client_state.name == "CONNECTED":
                    await websocket.receive_text()
                
        except WebSocketDisconnect:
            await host.disconnect(new_id)
    

    public_data_manager: ConnectionManager = ConnectionManager(2)
    @app.websocket("/public-view/{client_id}")
    async def public_views(websocket: WebSocket, client_id: int):
        await public_data_manager.connect(client_id, websocket)
        if players_middleware.connections_amount() == 2 and public_data_manager.connections_amount() == 2:
            await brodcast_public_data(public_data_manager)
        try:
            while True:
                await websocket.receive_text()
                
        except WebSocketDisconnect:
            await public_data_manager.disconnect(client_id)

    async def brodcast_public_data(connection_managger: ConnectionManager):
        general_public_data:str = json.dumps(desk.get_general_view())
        await connection_managger.broadcast(general_public_data)


    desk: GameDesk = GameDesk()
    players_middleware: ConnectionManager = ConnectionManager(2)
    @app.websocket("/playground/{id}")
    async def start_game(websocket: WebSocket, id: int):
        print(f"{id} arrived")
        await players_middleware.connect(int(id), websocket)

        if players_middleware.connections_amount() == 2:
            print("THERE ARE TWO")
            desk.init_row()
            await send_players_status(desk, players_middleware)
        try:
            while True:  # keep this socket alive forever
                raw = await websocket.receive_text()

                player_action: ActionPayload = json.loads(raw)
                print("player action received: ", player_action)
                print(type(player_action["card_index"]))
                
                new_action = PlayersActions(**player_action)
                desk.receive_players_action(id, new_action)
                await send_players_status(desk, players_middleware)
                await brodcast_public_data(public_data_manager)
        except WebSocketDisconnect:
            await players_middleware.disconnect(id)




