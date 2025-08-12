from random import randint
from constants.types import *
from classes.player import Player

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


def handle_cards_based_on_who_is_hand(player_1: Player, player_2: Player, deck: Deck) -> dict[str, Deck]:
    '''Depending on who's receiving the cards first, you might have more chances on having a better play'''
    cards_in_use: Deck = []
    if player_1.is_hand:
        player_1.cards = handle_cards(deck, cards_in_use)
        player_2.cards = handle_cards(deck, cards_in_use)
    else:
        player_2.cards = handle_cards(deck, cards_in_use)   
        player_1.cards = handle_cards(deck, cards_in_use)
   
    
        