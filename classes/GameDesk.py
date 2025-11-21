from constants.types import *
from classes.TrucoDeck import *
from classes.Player import Player
class GameDesk:
    # player_0: Player
    # player_1: Player
    # deck: TrucoDeck

    def __init__(self) -> None:
        self.deck = TrucoDeck()
        self.deck.create_deck()
        self.player_0 = Player()
        self.player_1 = Player()

    def play_with_players_status(self) -> list[dict[str, int | list[dict[str, int | str]]]]:
        new_row_cards: list[list[Card]] = self.deck.shuffle_cards()
        self.player_0.set_cards(new_row_cards[0])
        self.player_1.set_cards(new_row_cards[1])
        res = [self.player_0.show_player_data(), self.player_1.show_player_data()]
        self.player_0.add_points(1)
        self.player_1.add_points(1)
        return res

       