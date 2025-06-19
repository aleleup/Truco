from random import randint

def handle_cards(deck: list, cards_in_use: list) -> list:
    '''Searches in deck randomly a card and when 3 were selected = returns the hand'''
    i: int = 1
    res: list[dict[str, str|int]] = []
    while i <=3 :
        card_index: int = randint(0, 39)
        card : dict[str, int|str] = deck[card_index]

        if card not in cards_in_use:
            res.append(card)
            cards_in_use.append(card)
            i+=1
    
    return res
        