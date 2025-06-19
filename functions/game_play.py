from functions.deal_cards import handle_cards
def game_play(deck: list, ):
    cards_of_the_hand: list = []
    player_options = handle_cards(deck, cards_of_the_hand)
    pc_options = handle_cards(deck, cards_of_the_hand)

    for player in [player_options, pc_options]:
        print('================================')
        for card in player:
            print(f'{card['name']} -> {card['card_ascii_art']}')