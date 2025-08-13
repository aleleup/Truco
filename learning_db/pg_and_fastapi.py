from fastapi import APIRouter
from database import SessionLocal
from learning_db.models import MyExample
router = APIRouter()
db = SessionLocal()

@router.get("/test-api-example/{page_id}")
async def test_api_example(page_id: str):
    page_id: int = int(page_id)
    page_id_in_table: object = db.query(MyExample).filter(MyExample.player_id == page_id).all()

    print(f"Resultado del filtro: {page_id_in_table}")
    if page_id_in_table:
        return {
            "statusCode": 500,
            "message": "Ya hay alguien ocupando esta pagina",
            "available": False
        }
    
    new_player = MyExample(player_id=int(page_id))
    db.add(new_player)
    db.commit()
    db.refresh(new_player)
    print(f"Nuevo usuario registrado: {new_player.id}")
    return {
        "statusCode": 200,
        "message": "Usuario nuevo guardado con éxito",
        "available": True
    }


