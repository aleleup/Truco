class PlayersActions:
    def __init__(self, card_index: int, bet: list[str]) -> None:
        self.card_index: int = card_index
        self.bet: list[str] = bet