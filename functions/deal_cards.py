from random import randint
from constants.types import *
def handle_cards(deck: Deck, cards_in_use: Deck) -> Deck:
    '''Searches in deck randomly a card and when 3 were selected = returns the hand'''
    i: int = 1
    res: Deck = []
    while i <=3 :
        card_index: int = randint(0, 39)
        card: Card = deck[card_index]

        if card not in cards_in_use:
            res.append(card)
            cards_in_use.append(card)
            i+=1
            
    return res


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
    
        