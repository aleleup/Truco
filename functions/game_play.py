from random import randint
from functions.deal_cards import handle_cards
# from functions.start_up_functions import calc_envido
from classes.player import Player
from classes.bot import Bot
from constants.types import *

def game_stop(player:Player, bot:Bot) -> bool:
    if player.points == 30 or bot.points == 30:
        return True
    return False


def handle_cards_based_on_who_is_hand(players_id: int, bots_id: int, game_num:int, deck: Deck) -> dict[str, Deck]:
    '''Depending on who's receiving the cards first, you might have more chances on having a better play'''
    players_cards: Deck = []
    bots_cards: Deck = []
    cards_in_use: Deck = []
    if game_num % 2 == players_id:
        players_cards = handle_cards(deck, cards_in_use)
        bots_cards = handle_cards(deck, cards_in_use)
    else:
        bots_cards = handle_cards(deck, cards_in_use)
        players_cards = handle_cards(deck, cards_in_use)
    
    return {
        'players_cards': players_cards, 'bots_cards': bots_cards 
    }

def handle_envido_points(player: Player, bot: Bot, envido_calls_history: dict[str, int]):
    if player.total_envido > bot.total_envido or  (player.total_envido == bot.total_envido and player.is_hand) : 
         player.add_envido_points(envido_calls_history)
    if bot.total_envido > player.total_envido  or (player.total_envido == bot.total_envido and bot.is_hand ):
         bot.add_envido_points(envido_calls_history)
    

def game_play(deck: Deck, ):
    '''Contain all gameplay logic'''
    #total games played and turns
    game_num: int = 0
    player_id: int = randint(0, 1)
    bot_id: int = 1 - player_id

    # players points


    # instance players and methods here.
    player: Player = Player([], player_id, game_num, 30)
    bot: Bot = Bot([], bot_id, game_num, 30)

    while not game_stop(player, bot):
        game_num+=1
        cards_of_the_hand: dict[str, Deck] = handle_cards_based_on_who_is_hand(player_id, bot_id, game_num, deck)
        player.cards = cards_of_the_hand['players_cards']
        bot.cards = cards_of_the_hand['bots_cards']
       

        player.calc_envido()
        bot.calc_envido()



        hand: int = 0
        #envido instance:
        if len(player.cards) == len(bot.cards) and len(player.cards) == 3:
            hand = 1
            envidos_calls: dict[str, int] = {
                'Envido': 0,
                'real_envido': 0,
                'Falta Envido': 0
            }
            # play_envido(player, bot)
        if len(player.cards) == len(bot.cards) and len(player.cards) == 2:
            hand = 2
        if len(player.cards) == len(bot.cards) and len(player.cards) == 1:
            hand = 3

        break
