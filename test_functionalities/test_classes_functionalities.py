from classes.bot import Bot
from classes.player import Player
from functions.deal_cards import handle_cards
from  constants.types import *
from math import factorial as f



def test_first_hand(deck):
    player_id: int = 0
    player_2_id: int = 1 

    player: Player = Player([], player_id, 1, 30)
    player_2: Player = Player([], player_2_id, 1, 30)

    cards_in_use = []
    player.cards = handle_cards(deck, cards_in_use)
    player_2.cards = handle_cards(deck, cards_in_use)
    player.calc_envido()
    player_2.calc_envido()
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


    hand: int = 1
    while True:
        players_last_movement: Movement = {
            'is_bet' : False, 'player_action': ''
        }

        players_last_movement = player.play_card(players_last_movement, hand, envidos_calls_history, truco_calls_history)   
        print(players_last_movement['player_action'] if players_last_movement['is_bet'] else players_last_movement['player_action']['card_ascii_art'] )

        players_last_movement = player_2.play_card(players_last_movement, hand, envidos_calls_history, truco_calls_history)
        print(players_last_movement['player_action'] if players_last_movement['is_bet'] else players_last_movement['player_action']['card_ascii_art'] )
        
        hand += 1

        
def cards_in_hand_in_comb_list(cards_in_hand, comb_list):
    counter = 0
    for comb in comb_list:
        for card in cards_in_hand:
            if card in comb: 
                counter += 1
        if counter == 3: return True
    
    return False
def test_avarage_to_stablish_thresholds(deck):
    bot = Bot([], 0, 1, 30)
    i: int = 0
    cards_comb: list[Deck] = []
    total_combinations_possible:int = 9880 #combinatory (40,  3)

    while i < total_combinations_possible:
        bot.cards = handle_cards(deck, [])
        if not cards_in_hand_in_comb_list(bot.cards, cards_comb):
            cards_comb.append(bot.cards)


            print(f'''
                ####### CARDS #######
                {bot.cards[0]['name']} | {bot.cards[1]['name']} | {bot.cards[2]['name']}
            ''')
            i += 1
   