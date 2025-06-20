from random import randint
from functions.deal_cards import handle_cards
from functions.start_up_functions import calc_envido
def create_player_options(cards: list[dict],player_num: int, game_num: int, falta_envido_val:int) -> dict[str, list|int|str|bool]:
    return {
        'cards': cards,
        'total_envido': calc_envido(cards),
        'is_hand': True if game_num %2 == player_num else False,
        'envido_options': {
            'Envido': 2,
            'Real Envido': 3,
            'Falta Envido': falta_envido_val
        },
        'truco_options': {
            'Truco': 2,  ## Only truco available
            'Re Truco': 3,
            'Vale Cuatro': 4
        },
        
        
    }


def game_play(deck: list, ):
    '''Contain all gameplay logic'''
    #total games played and turns
    game_num: int = 0
    game_starter: int = randint(0, 1)
    game_starter_2: int = 1 - game_starter

    # players points
    player_points: int = 0
    pc_points: int = 0

    # cards handler
    cards_of_the_hand: list[dict] = []
    player_cards: list[dict] = handle_cards(deck, cards_of_the_hand)
    pc_cards: list[dict] = handle_cards(deck, cards_of_the_hand)


    player_options = create_player_options(player_cards, game_starter, game_num, 30 - pc_points )
    pc_options = create_player_options(pc_cards, game_starter_2, game_num,30 - player_points)



   
    for player in [player_options, pc_options]:
        print('================================')
        for card in player['cards']:
            print(f'{card['name']} -> {card['card_ascii_art']}')
        print('TOTAL ENVIDO', player['total_envido'])