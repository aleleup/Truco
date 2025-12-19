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

CardDict = dict[str, str | int]

#####################################
PlayerStatus = dict[str, int | list[dict[str, int | str]] | PlayerOptions]
PlayerActionResponse = dict[str, int | dict[int, str]]
PlayerPublicData = dict[str, int | list[CardDict] | str]

