from random import randint
from functions.deal_cards import handle_cards
# from functions.start_up_functions import calc_envido
from classes.player import Player
from classes.bot import Bot
from classes.player_basics import PlayerBasics

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

def handle_envido_points(hand_player:PlayerBasics,  other_player:PlayerBasics, envido_calls_history: dict[str, int], bets_on_table:dict[int, str]):
    bets_values: list[str] = bets_on_table.values()
    if 'accept' in bets_values:
        if hand_player.total_envido >= other_player.total_envido: 
            hand_player.add_envido_points(envido_calls_history)
        else:
            other_player.add_envido_points(envido_calls_history)
    if 'dont_accept' in bets_values:
        if bets_on_table[hand_player.player_num] == 'dont_accept':
            other_player.add_unwanted_envido_points(envido_calls_history)
        else:
            hand_player.add_unwanted_envido_points(envido_calls_history)

    

def play_envido(hand_player:PlayerBasics, other_player:PlayerBasics) -> None:
    '''hand_player starts the envido bets and the bet rices depending on other_players decisions'''
    envidos_calls: dict[str, int] = {
                'envido': 0,
                'real_envido': 0,
                'falta_envido': 0
            }
    hand_player_num: int = hand_player.player_num
    other_player_num: int = other_player.player_num

    bets_on_table: dict[int, str] = {
        hand_player_num: '',
        other_player_num: ''
    }
    while bets_on_table[other_player_num] not in ['accept', 'dont_accept'] :
            
            bets_on_table[hand_player_num] = hand_player.ask_envido(envidos_calls, bets_on_table[other_player_num])
            print(f"hand player says {bets_on_table[hand_player_num]}")

            if bets_on_table[hand_player_num] in ['accept', 'dont_accept']: break 

            bets_on_table[other_player_num] = other_player.ask_envido(envidos_calls, bets_on_table[hand_player_num])
            print(f"other player says {bets_on_table[other_player_num]}")
    print('###############################################################')

    handle_envido_points(hand_player, other_player, envidos_calls, bets_on_table)

    


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
            if player.is_hand:
                play_envido(player, bot)
            else: play_envido(bot, player)

        print(f"PLAYER ENVIDO: {player.total_envido} || BOT ENVIDO {bot.total_envido}")

        # if len(player.cards) == len(bot.cards) and len(player.cards) == 2:
        #     hand = 2
        # if len(player.cards) == len(bot.cards) and len(player.cards) == 1:
        #     hand = 3

        print(f"PLAYER POINTS: {player.points} || BOT POINTS {bot.points}")
