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
        