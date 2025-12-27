from typing import TypedDict, List
from pydantic import BaseModel
type Bet = str
type PlayerOptions = dict[str, str | list[str]]
###### NEW METHODOLOGY TO IMPLEMENT
class ActionPayload(TypedDict):
    card_index: int
    bet: List[str]
#### Players Actions ####
class PlayersActions(BaseModel):
    card_index: int
    bet: list[Bet]

type CardDict = dict[str, str | int]

#####################################
type PlayerStatus = dict[str, int | list[dict[str, int | str]] | PlayerOptions]
type PlayerActionResponse = dict[str, int | dict[int, str]]
type PlayerPublicData = dict[str, int | list[CardDict] | str]
type PublicData = dict[str, list[PlayerPublicData] | bool | int]
