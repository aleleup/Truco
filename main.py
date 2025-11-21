from fastapi import FastAPI
from connections import users_example
from classes.GameDesk import GameDesk
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

@app.get("/cards")
def show_cards():
    return desk.play_with_players_status()

if __name__ == "__main__":
    print("STARTING TRUCO")
    