from classes.Card import Card
class Player():
    def __init__(self) -> None:
        self._cards: list[Card]
        self._points: int = 0

    def show_card(self) -> list[dict[str, str | int]]: 
        res: list[dict[str, str | int]] = []
        for card in self._cards:
            card_data: dict[str, str | int] = {
                'name': card.name,
                'value': card.value,
                'type': card.type,
                'envido_value': card.envido_value
            }
            res.append(card_data)
        return res
    

    def set_cards(self, cards: list[Card]) -> None:
        self._cards = cards

    def add_points(self, points: int):
        self._points += points


    def show_player_data(self) -> dict[str, int | list[dict[str, int | str]]]:
        return {
            "points": self._points,
            "cards": self.show_card()
        }