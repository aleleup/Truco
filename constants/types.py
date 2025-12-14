from typing import TypedDict, List
from pydantic import BaseModel

Bet = str
PlayerOptions = dict[str, str | list[str]]
###### NEW METHODOLOGY TO IMPLEMENT
class ActionPayload(TypedDict):
    card_index: int
    bet: List[str]
#### Players Actions ####
class PlayersActions(BaseModel):
    card_index: int
    bet: list[Bet]
# class PlayerStatus(BaseModel):
#     player_id: int
#     points: int
#     cards: int
#     options: PlayerOptions
#     envido: int
#     is_player_turn: bool

#####################################
PlayerStatus = dict[str, int | list[dict[str, int | str]] | PlayerOptions]
PlayerActionResponse = dict[str, int | dict[int, str]]
# Movement = dict[str, bool | PlayerAction]
# Options = dict[int, Card | Bet]
