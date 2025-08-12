from random import randint
from classes.player import Player
# from classes.player_2 import Player
from constants.types import *
from functions.deal_cards import handle_cards_based_on_who_is_hand
from functions.envido_functions import *


def game_over(player_1:Player, player_2:Player) -> bool:
    if player_1.points >= 30 or player_2.points >= 30:
        return True
    return False

def set_back_players_last_mov_on_accept_or_dont_accept(player_last_movement: Movement) -> None:
    if not player_last_movement['is_bet']: return

    if player_last_movement['player_action'] in ['accept', 'dont_accept']:
        player_last_movement['player_action'] = ''
        player_last_movement['is_bet'] = False
        
def game_play(deck: Deck):
    '''Contain all gameplay logic. For now on, It's a pvp'''

    game_num: int = 0
    player_1_id: int = randint(0, 1)
    player_2_id: int = 1 - player_1_id

    player_1 = Player([], player_1_id, game_num, 30)
    player_2 = Player([], player_2_id, game_num, 30)
    while not game_over(player_1, player_2):
        game_num+=1
        handle_cards_based_on_who_is_hand(player_1, player_2, deck)
        truco_calls_history: dict[str, int] = {
                'truco': 0,
                're_truco': 0,
                'vale_cuatro': 0
            }
        envidos_calls_history: dict[str, int] = {
                'envido': 0,
                'real_envido': 0,
                'falta_envido': 0
            }
        player_1.calc_envido()
        player_2.calc_envido()

        hand: int = 1

        players_last_movement: Movement = {
            'is_bet' : False, 'player_action': ''
        }

        while player_1.cards and player_2.cards:
            players_last_movement = player_1.play_card(players_last_movement, hand, envidos_calls_history, truco_calls_history)   
            print("player_1: ", players_last_movement['player_action'] if players_last_movement['is_bet'] else players_last_movement['player_action']['card_ascii_art'] )

            set_back_players_last_mov_on_accept_or_dont_accept(players_last_movement)

            players_last_movement = player_2.play_card(players_last_movement, hand, envidos_calls_history, truco_calls_history)
            print("player_2: ", players_last_movement['player_action'] if players_last_movement['is_bet'] else players_last_movement['player_action']['card_ascii_art'] )

            set_back_players_last_mov_on_accept_or_dont_accept(players_last_movement)
            if not players_last_movement['is_bet']:
                hand += 1

