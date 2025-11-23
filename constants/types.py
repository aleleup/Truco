# Card = dict[str, str | int]
# Deck = list[Card]
Bet = str
PlayerOptions = dict[str, list[str] | str]
PlayerStatus = dict[str, int | list[dict[str, int | str]] | PlayerOptions]
PlayerActionResponse = dict[str, int | list[str]]
# Movement = dict[str, bool | PlayerAction]
# Options = dict[int, Card | Bet]
