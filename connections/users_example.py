import json
from fastapi import APIRouter
from connections.items_whith_class_example import TestUsersWithFastApi
router = APIRouter(prefix="/users", tags=["users"])
test = TestUsersWithFastApi()

@router.get("/")
def get_users():
    return [{"name": "Alice"}, {"name": "Bob"}]

@router.get("/testing-class-state")
def class_state():
    return {"new_items": test.show_items_changing_iterator()}

@router.get("/testing-class/{item}")
def x(item:int):
    return json.dumps({"show-item": test.show_item(item)})


@router.get("/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}

