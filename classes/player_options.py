# from random import randint
# from functions.deal_cards import handle_cards
from functions.start_up_functions import calc_envido

class PlayerOptions:
    def __init__(self, cards: list[dict], player_num: int, game_num: int, falta_envido_val:int):
        self.cards = cards
        self.player_num = player_num
        self.game_num = game_num
        self.falta_envido_val = falta_envido_val
        self.total_envido: int = calc_envido(cards)
        self.is_hand: bool =  True if game_num %2 == player_num else False    
        self.envido_options: dict[str, int] = {
            'envido': 2,
            'real_envido': 3,
            'falta_envido': falta_envido_val
        },
        self.truco_options: dict[str, int] = {
            'truco': 2,  ## Only truco available
            're_truco': 3,
            'vale_cuatro': 4
        },

    def play_envido(self):
        pass


player_test = PlayerOptions([{}, {}, {}], 1, 1, 30)


print(player_test.player_num)


