import json, asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from classes.GameDesk import GameDesk
from classes.ConnectionManager import ConnectionManager
from constants.types import *
from fastapi.middleware.cors import CORSMiddleware

# from classes.TrucoDeck import TrucoDeck
############# AUX-FUNCTIONS #############
async def send_players_status(game_desk:GameDesk, connection_manager: ConnectionManager):
    for id in [0,1]: 
            status: PlayerStatus = game_desk.player_status(id)
            await connection_manager.send_to(id, json.dumps(status))
            await asyncio.sleep(0.2)


####### USAGE OF WEB-SOCKETS #######
if __name__ == "main":

    app = FastAPI()
    app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    desk_per_session: dict[int, GameDesk] = {}
    public_manager_per_session: dict[int, ConnectionManager] = {}
    private_manager_per_session: dict[int, ConnectionManager] = {}
    host_per_session: dict[int, ConnectionManager] = {}

    @app.get("/store-session-id/{session}")
    async def store_session_id(session: int):
        if session not in host_per_session:
            host_per_session[session] = ConnectionManager(2)
        return {"message": "session already stored"}

    ### KEEP CLIENTS IN LOBBY UNTIL TWO PLAYERS ARE CONNECTED (There's no need to use databases for this logic now)
    @app.websocket("/enter-lobby/{session}/{id}")
    async def receive_player(websocket: WebSocket, id:str, session: int):
        host: ConnectionManager = host_per_session[session]
        new_id: int = 1 if host.connections_amount() > 0 else 0
        print("CONNECTION NEW ID", new_id)
        await host.connect(new_id, websocket) # send them into the lobby and return their new id
        await host.send_to(new_id, json.dumps({"new_id": new_id}))
        
        try:
            if host.connections_amount() == 2:
                desk_per_session[session] = GameDesk()
                public_manager_per_session[session] = ConnectionManager(2)
                private_manager_per_session[session] = ConnectionManager(2)
                await host.broadcast(json.dumps({"allow_access": True}))

                # Give the OS time to flush frames --> AI HELP
                await asyncio.sleep(0.2)

                await host.shutdown()
                return
            while True:
                if websocket.client_state.name == "CONNECTED":
                    await websocket.receive_text()
                
        except WebSocketDisconnect:
            await host.shutdown()


    @app.websocket("/public-view/{session}/{client_id}")
    async def public_views(websocket: WebSocket, client_id: int, session: int):
        public_data_manager: ConnectionManager = public_manager_per_session[session]
        private_data_manager: ConnectionManager = private_manager_per_session[session]
        await public_data_manager.connect(client_id, websocket)
        if private_data_manager.connections_amount() == 2 and public_data_manager.connections_amount() == 2:
            await brodcast_public_data(public_data_manager, session)
        try:
            while True:
                await websocket.receive_text()
                
        except WebSocketDisconnect:
            await public_data_manager.shutdown()
            delete_desk_and_manager_at_session(session)

    async def brodcast_public_data(connection_managger: ConnectionManager, session: int):
        desk: GameDesk = desk_per_session[session]
        private_data_manager: ConnectionManager = private_manager_per_session[session]

        general_data: PublicData = desk.get_general_view()
        await connection_managger.broadcast(json.dumps(general_data))
        

        if general_data["winner_id"] != -1:
            return delete_desk_and_manager_at_session(session)

        if general_data["round_winner"] != -1:
            # STARTING DANGEROUS RECURSION
            await asyncio.sleep(3)
            desk.init_round()
            await send_players_status(desk, private_data_manager)
            await brodcast_public_data(connection_managger, session) # NOW general_data["round_winner"] == -1




    @app.websocket("/playground/{session}/{id}")
    async def start_game(websocket: WebSocket, id: int, session: int):
        desk: GameDesk = desk_per_session[session]
        private_data_manager: ConnectionManager = private_manager_per_session[session]
        public_data_manager: ConnectionManager = public_manager_per_session[session]

        print(f"{id} arrived")
        await private_data_manager.connect(int(id), websocket)

        if private_data_manager.connections_amount() == 2:
            print("THERE ARE TWO")
            desk.init_round()
            await send_players_status(desk, private_data_manager)
        try:
            while True:  # keep this socket alive forever
                raw = await websocket.receive_text()

                player_action: ActionPayload = json.loads(raw)
                print("player action received: ", player_action)
                
                new_action = PlayersActions(**player_action)
                desk.receive_players_action(id, new_action)
                await send_players_status(desk, private_data_manager)
                await brodcast_public_data(public_data_manager, session)
        except WebSocketDisconnect:
            await private_data_manager.shutdown()
            delete_desk_and_manager_at_session(session)

    def delete_desk_and_manager_at_session(session: int):
        del desk_per_session[session]
        del public_manager_per_session[session]
        del private_manager_per_session[session]
