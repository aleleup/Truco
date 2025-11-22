from constants.types import *
from classes.TrucoDeck import *
from classes.Player import Player
class GameDesk:
    # player_0: Player
    # player_1: Player
    # deck: TrucoDeck

    def __init__(self) -> None:
        self._deck = TrucoDeck()
        self._deck.create_deck()
        self._player_0 = Player(0)
        self._player_1 = Player(1)
        self._bet_values: dict[str, dict[str, int]] = {
            'envido': {
                'envido': 2,
                'real_envido':3,
                # 'falta_envido': 0 Updates dinamically
            },
            'truco':{
                'truco': 2,
                're_truco': 3,
                'vale_cuatro': 4
            }
        }
        self._ACCEPT = 'accept'
        self._DONT_ACCEPT = 'dont_accept'
        self._round: int = 0
        self._hand_player: Player
        self._foot_player: Player


    def _set_hand_and_foot_players(self) -> None:
        if self._round % 2 == 0:
            self._hand_player = self._player_0
            self._foot_player = self._player_1
        else:
            self._hand_player = self._player_1
            self._foot_player = self._player_0 

    def init_row(self) -> list[PlayerStatus]:
        self._round += 1
        new_row_cards: list[list[Card]] = self._deck.shuffle_cards()
        self._set_hand_and_foot_players()
        self._hand_player.set_cards(new_row_cards[0])
        self._foot_player.set_cards(new_row_cards[1])
        res = [self._hand_player.show_player_data(), self._foot_player.show_player_data()]
        return res


    def show_player_data_by_id(self, id: int) -> PlayerStatus:
        if id == 0:
            return self._player_0.show_player_data()
        else:
            return self._player_1.show_player_data() 
        
