from fastapi import FastAPI
from connections import users_example
from classes.GameDesk import GameDesk
from classes.PlayersActions import PlayersActions
from constants.types import *
from pydantic import BaseModel

class Item(BaseModel):
    id: int
    action: dict[str, int | list[str]]

app = FastAPI()
app.include_router(users_example.router)
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
def player_throws_card(body: Item):
   if type(body.action["card_index"]) == int and type(body.action["bet"]) == list:
        new_action = PlayersActions(body.action["card_index"], body.action["bet"])
        return desk.receive_players_action(body.id, new_action)
    

@app.get("/player/{id}")
def player_by_id(id: int):
    return desk.show_player_data_by_id(id)


