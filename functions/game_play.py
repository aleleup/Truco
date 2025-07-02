from random import randint
from functions.deal_cards import handle_cards
from functions.start_up_functions import calc_envido
from classes.player_options import PlayerOptions
from classes.bot import Bot
def game_stop(player_points: int, pc_points: int) -> bool:
    if player_points == 30 or pc_points == 30:
        return True
    return False


def handle_cards_based_on_who_is_hand(players_id: int, bots_id: int, game_num:int, deck: list[dict]) -> dict[str, list[dict]]:
    '''Depending on who's receiving the cards first, you might have more chances on having a better play'''
    players_cards: list[dict] = []
    bots_cards: list[dict] = []
    cards_in_use: list[dict] = []
    if game_num % 2 == players_id:
        players_cards = handle_cards(deck, cards_in_use)
        bots_cards = handle_cards(deck, cards_in_use)
    else:
        bots_cards = handle_cards(deck, cards_in_use)
        players_cards = handle_cards(deck, cards_in_use)
    
    return {
        'players_cards': players_cards, 'bots_cards': bots_cards 
    }


def game_play(deck: list, ):
    '''Contain all gameplay logic'''
    #total games played and turns
    game_num: int = 0
    player_id: int = randint(0, 1)
    bot_id: int = 1 - player_id

    # players points
    player_points: int = 0
    pc_points: int = 0

    # instance players and methods here.
    player_options = PlayerOptions([], player_id, game_num, 30)
    bot_options = Bot([], bot_id, game_num, 30)

    while not game_stop(player_points, pc_points):
        game_num+=1
        cards_of_the_hand: dict[str, list] = handle_cards_based_on_who_is_hand(player_id, bot_id, game_num, deck)
        player_options.cards = cards_of_the_hand['players_cards']
        bot_options.cards = cards_of_the_hand['bots_cards']
       



        hand: int = 0
        #envido instance:
        if len(player_options.cards) == len(bot_options.cards) and len(player_options.cards) == 3:
            hand = 1
            envidos_calls: dict[str, int] = {
                'Envido': 0,
                'real_envido': 0,
                'Falta Envido': 0
            }
            # play_envido(player_options, bot_options)
        if len(player_options.cards) == len(bot_options.cards) and len(player_options.cards) == 2:
            hand = 2
        if len(player_options.cards) == len(bot_options.cards) and len(player_options.cards) == 1:
            hand = 3

        break
