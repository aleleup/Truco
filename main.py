from functions.card_creation import create_deck
from functions.game_play import game_play
from test_functionalities.test_classes_functionalities import *
from fastapi import FastAPI
# from learning_db import pg_and_fastapi
from connections import connections
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import SessionLocal
from databases.tables_schemas import PlaygroundTable, GameTableTable
from constants.status import *
# Crear una instancia de la aplicación FastAPI
app = FastAPI()
db = SessionLocal()

#TODO: Learn how to create types based only in the variable value. f.e: status type must only in [on_going, finished]; bet type must be [envido, truco, accept, ...]
origins = [
    "http://localhost", 
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los headers
)
# app.include_router(pg_and_fastapi.router)
app.include_router(connections.router)
@app.get("/")
def read_root() -> dict[str, str]:
    """
    Función que se ejecuta cuando se hace una petición GET a la URL raíz.
    Devuelve un diccionario, que FastAPI convierte automáticamente a JSON.
    """
    return {"Hello": "World"}

