Card = dict[str, str or int]
Deck = list[Card]
Bet = str
PlayerAction = Card or Bet
Movement = dict[str, bool or PlayerAction]
Options = dict[int, Card or Bet]
