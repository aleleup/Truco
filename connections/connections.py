from pydantic import BaseModel
from database import SessionLocal
from databases.tables_schemas import PlaygroundTable, GameTableTable
from constants.status import *
from fastapi import APIRouter

router = APIRouter()
db = SessionLocal()
def check_starting_game() -> bool:
    play_ground_table_items: int = db.query(PlaygroundTable).count()
    if play_ground_table_items != 2:
        return False
    game_table_table = GameTableTable(status=ON_GOING, player_0_points=0,  player_1_points=0)
    db.add(game_table_table)
    db.commit()
    db.refresh(game_table_table)    
    return True

class PageAvailabilityBody(BaseModel):
    '''Defining body structure'''
    pageId:int
    
@router.post("/check_playground_availability")
async def check_playground_availability(body: PageAvailabilityBody):
    print("PAYLOAD INCOMMING", body)
    page_id: int = body.pageId
    page_id_in_table: list[PlaygroundTable] = db.query(PlaygroundTable).filter(PlaygroundTable.playground_id == page_id).all()

    print(f"Resultado del filtro: {page_id_in_table}")
    if page_id_in_table:
        return {
            "statusCode": 500,
            "message": "Ya hay alguien ocupando esta pagina",
            "available": False,
            "startingGame": False

        }
    
    new_player = PlaygroundTable(playground_id=int(page_id))
    db.add(new_player)
    db.commit()
    db.refresh(new_player)
    print(f"New user registered: {new_player.id}")
    return {
        "statusCode": 200,
        "message": "Usuario nuevo guardado con éxito",
        "available": True,
        "startingGame": check_starting_game()
    }


@router.post("/delete-playground")
async def delete_playground(body: PageAvailabilityBody):
    print("PAYLOAD INCOMMING", body)
    item_to_delete: PlaygroundTable = db.query(PlaygroundTable).filter(PlaygroundTable.playground_id == body.pageId).first()
    if not item_to_delete:
        return {
            "statusCode": 500,
            "message": "None user found",
            "error": True
        },

    db.delete(item_to_delete)
    db.commit()
    return {
        "statusCode": 200,
        "message": "User deleted succesfully",
        "error": False
    }
    