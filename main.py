from functions.card_creation import create_deck
from functions.game_play import game_play
from test_functionalities.test_classes_functionalities import *
from fastapi import FastAPI
from learning_db import pg_and_fastapi
# Crear una instancia de la aplicación FastAPI
app = FastAPI()


app.include_router(pg_and_fastapi.router)
# Definir el primer "endpoint" (punto de acceso) de la API
# El decorador @app.get("/") asocia la función de abajo con la URL raíz "/"
@app.get("/")
def read_root() -> dict[str, str]:
    """
    Función que se ejecuta cuando se hace una petición GET a la URL raíz.
    Devuelve un diccionario, que FastAPI convierte automáticamente a JSON.
    """
    return {"Hello": "World"}

# # Puedes agregar más endpoints fácilmente
# @app.get("/items/{item_id}")
# def read_item(item_id: str, q: str = None) -> dict[str, str]:
#     """
#     Endpoint que toma un parámetro de ruta (item_id) y un parámetro de consulta (q).
#     """
#     if q:
#         return {"item_id": item_id, "q": q}
#     return {"item_id": item_id}


# def render_truco() -> None:
#     '''Orquestator and renderer of the game'''

#     # root = tk.Tk()
#     # root.geometry('700x500')

#     # display_text = tk.Label(root=root, value=constants['title'])

#     deck = create_deck()
#     # print(deck)
#     game_play(deck)
#     # test_bot_ask_truco(deck)
# render_truco()


