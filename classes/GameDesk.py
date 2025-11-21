from constants.types import *
from classes.TrucoDeck import *
class GameDesk:
    # player_0: Player
    # player_1: Player
    # deck: TrucoDeck

    def __init__(self) -> None:
        self.deck = TrucoDeck()
        self.deck.create_deck()


    def deal_cards(self):
        return self.deck.shuffle_cards()

       