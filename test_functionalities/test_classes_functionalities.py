from classes.bot import Bot
from classes.player import Player
from functions.deal_cards import handle_cards
from  constants.types import *




def test_first_hand(deck):
    player_id: int = 0
    bot_id: int = 1 

    player: Player = Player([], player_id, 1, 30)
    bot: Bot = Bot([], bot_id, 1, 30)
    cards_in_use = []
    player.cards = handle_cards(deck, cards_in_use)
    bot.cards = handle_cards(deck, cards_in_use)
    player.calc_envido()
    bot.calc_envido()
    truco_calls_history: dict[str, int] = {
            'truco': 1,
            're_truco': 0,
            'vale_cuatro': 0
        }
    envidos_calls_history: dict[str, int] = {
            'envido': 0,
            'real_envido': 0,
            'falta_envido': 0
        }


    hand: int = 1

    players_last_movement: Movement = {
        'is_bet' : False, 'player_action': ''
    }

    players_last_movement = player.play_card(players_last_movement, hand, envidos_calls_history, truco_calls_history)

    print(players_last_movement['player_action'] if players_last_movement['is_bet'] else players_last_movement['player_action']['card_ascii_art'] )
    print("TRUCO_HISTORY_MODIFICATION", truco_calls_history)