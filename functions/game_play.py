from random import randint
from classes.player import Player
from classes.bot import Bot
from constants.types import *
from functions.deal_cards import handle_cards_based_on_who_is_hand
from functions.envido_functions import *


def game_over(player:Player, bot:Bot) -> bool:
    if player.points >= 30 or bot.points >= 30:
        return True
    return False

def game_play(deck: Deck):
    '''Contain all gameplay logic'''

    '''
        TODO:   Integrate and combine envido and cards play. Now they are going to be separated, but I expect that with a few changes in all
                functions and methds involved the integration will be simple for v1 
    '''
    
    #total games played and turns
    game_num: int = 0
    player_id: int = randint(0, 1)
    bot_id: int = 1 - player_id

    # players points
    #TODO optimize instantiation of players -> idea: instance players once and then create functions that updates if player is or is not hand  
    player: Player = Player([], player_id, game_num, 30)
    bot: Bot = Bot([], bot_id, game_num, 30)
    while not game_over(player, bot):
        game_num+=1
        is_in_envido: bool = False
        cards_of_the_hand: dict[str, Deck] = handle_cards_based_on_who_is_hand(player_id, bot_id, game_num, deck)
        player.cards = cards_of_the_hand['players_cards']
        bot.cards = cards_of_the_hand['bots_cards']
        truco_calls_history: dict[str, int] = {
                'truco': 0,
                're_truco': 0,
                'vale_cuatro': 0
            }
        envidos_calls: dict[str, int] = {
                'envido': 0,
                'real_envido': 0,
                'falta_envido': 0
            }
        player.calc_envido()
        bot.calc_envido()

        hand: int = 1

        players_last_movement: Movement = {
            'is_bet' : False, 'player_action': ''
        }

