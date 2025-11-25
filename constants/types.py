# Card = dict[str, str | int]
# Deck = list[Card]
Bet = str
PlayerOptions = dict[str, str | dict[int,str] | bool]
PlayerStatus = dict[str, int | list[dict[str, int | str]] | PlayerOptions]
PlayerActionResponse = dict[str, int | dict[int, str]]
# Movement = dict[str, bool | PlayerAction]
# Options = dict[int, Card | Bet]
