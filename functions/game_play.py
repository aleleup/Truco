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

def game_stop(player_points: int, pc_points: int) -> bool:
    if player_points == 30 or pc_points == 30:
        return True
    return False

def play_envido(p1_options: dict, p2_options: dict, envidos_calls: dict):
    
    p1_envido: int = p1_options['total_envido']
    p2_envido: int = p2_options['total_envido']
    envidos_in_zeros: bool =(
        envidos_calls['envido'] == envidos_calls['real_envido'] 
        and envidos_calls['envido'] == envidos_calls['falta_envido']
        and envidos_calls['envido'] == 0
        )
    while True:
        if p1_options['is_hand'] and envidos_in_zeros:
            envido: str = input("1:envido, 2: real, 3: falta")
            
                

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
    

    while not game_stop(player_points, pc_points):
        game_num+=1
        cards_of_the_hand: list[dict] = []
        player_cards: list[dict] = handle_cards(deck, cards_of_the_hand)
        pc_cards: list[dict] = handle_cards(deck, cards_of_the_hand)

        player_options = create_player_options(player_cards, game_starter, game_num, 30 - pc_points )
        pc_options = create_player_options(pc_cards, game_starter_2, game_num,30 - player_points)


        game_instance: int = 0
        #envido instance:
        if len(player_options['cards']) == len(pc_options['cards']) and len(player_options['cards']) == 3:
            game_instance = 1
            envidos_calls: dict[str, int] = {
                'Envido': 0,
                'real_envido': 0,
                'Falta Envido': 0
            }
            play_envido(player_options, pc_options)
        if len(player_options['cards']) == len(pc_options['cards']) and len(player_options['cards']) == 2:
            game_instance = 2
        if len(player_options['cards']) == len(pc_options['cards']) and len(player_options['cards']) == 1:
            game_instance = 3

