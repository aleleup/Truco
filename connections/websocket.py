# from pydantic import BaseModel
# from database import SessionLocal
# from databases.tables_schemas import PlaygroundTable, GameTableTable
from constants.status import *
from fastapi import APIRouter, WebSocket
from classes.game_table import GameTableClass
import json

router = APIRouter()
@router.websocket('/show_cards')
async def return_players_cards(websocket: WebSocket):
    print("TRYING TO STABLISH CONNECTION")
    await websocket.accept()
    try: 
        game_table = GameTableClass() 
        game_table.start_game()

        while not game_table.game_over(): 
            data = await websocket.receive_text()
            print(f"data incomming: {data}")
            data_to_send_to_the_front = {
                "p_0_cards": game_table.player_0.cards,
                "p_1_cards": game_table.player_0.cards

            }

            await websocket.send_json(json.dumps(data_to_send_to_the_front))
    except Exception as e:
        print(f'Exception found and connection lost', e)



# async def show_cards_logic(websocket: WebSocket):
#     '''only prints cards'''
#     try:
#         data = await websocket.receive_text()
#         print(f"data incomming: {data}")
#         game_table = GameTableClass() 
#         game_table.start_game()
#         data_to_send_to_the_front = {
#             "p_0_cards": game_table.player_0.cards,
#             "p_1_cards": game_table.player_0.cards

#         }
#         await websocket.send_json(json.dumps(data_to_send_to_the_front))
#     except Exception as e:
#         print("Error in show_cards_logic", e)