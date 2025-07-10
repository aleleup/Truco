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
        
        cards_of_the_hand: dict[str, Deck] = handle_cards_based_on_who_is_hand(player_id, bot_id, game_num, deck)
        player.cards = cards_of_the_hand['players_cards']
        bot.cards = cards_of_the_hand['bots_cards']
       

        player.calc_envido()
        bot.calc_envido()

        hand: int = 0

        if len(player.cards) == len(bot.cards) and len(player.cards) == 3:
            hand = 1
            if player.is_hand:
                play_envido(player, bot)
            else: play_envido(bot, player)

        print(f"PLAYER ENVIDO: {player.total_envido} || BOT ENVIDO {bot.total_envido}")

        # if len(player.cards) == len(bot.cards) and len(player.cards) == 2:
        #     hand = 2
        # if len(player.cards) == len(bot.cards) and len(player.cards) == 1:
        #     hand = 3

        print(f"PLAYER POINTS: {player.points} || BOT POINTS {bot.points}")
        print("####################################")
