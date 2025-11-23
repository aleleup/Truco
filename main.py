from fastapi import FastAPI
from connections import users_example
from classes.GameDesk import GameDesk

from pydantic import BaseModel

class Item(BaseModel):
    id: int
    index: int

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

@app.post("/throw-card")
def player_throws_card(body: Item):
    # return
    return desk.add_to_compare_list(int(body.id), int(body.index))
    

@app.get("/player/{id}")
def player_by_id(id: int):
    return desk.show_player_data_by_id(id)


