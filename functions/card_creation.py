from constants.constants import card_ascii_art
from constants.emojis import * 
def create_card_values(number: int,  type: str, value: int, envido_value: int) -> dict[str, int| str]:
    '''creats card dictonary by the params craeted'''
    emoji_store: dict[str, str] = {
        'sword': SWORD_EMOJI,
        'wood': WOOD_EMOJI,
        'gold': GOLD_EMOJI,
        'cup': CUP_EMOJI,
    } 
    return {
        'name': f'{number} {emoji_store[type]}',
        'type': type,
        'value': value,
        'envido_value': envido_value,
        'card_ascii_art': card_ascii_art[f'{number}&{type}']
    }

def calc_card_num(i: int) -> int:
    if i == 1:
        return 4
    if i == 2:
        return 5
    if i == 3:
        return 6
    if i in [4, 12, 11]:
        return 7
    if i == 5:
        return 10
    if i == 6:
        return 11
    if i == 7:
        return 12
    if i in [8, 13, 14]:
        return 1
    if i == 9:
        return 2
    if i == 10:
        return 3

def calc_envido_value(card_num: int) -> int:
    if card_num in [12, 11, 10]:
        return 0
    return card_num   

def add_to_deck(type_list: list[str], card_num:int, card_value: int, envido_value: int, deck: list):
    for type in type_list:
                deck.append(create_card_values(card_num, type, card_value, envido_value)) 

def create_deck() -> list[dict[str, int| str]]:
    '''logic_vals of cards:
        1 swrd == 14;
        1 wdd == 13;
        7 swrd == 12
        7 gld == 11
        *3 == 10
        *2 == 9
        1cup == 1gld == 8
        *12 == 7
        *11 == 6
        *10 == 5
        7cup == 7 wood == 4
        *6 == 3
        *5 == 2
        *4 == 1

    Based on that, I'll create the deck if all nums have same logic value and when it depends on the card type,
    i'll have no other than hardocode the value.

    '''
    deck: list = []
    for i in range(1, 15):
        card_num: int = calc_card_num(i)
        envido_value: int = calc_envido_value(card_num)
        # case all cards num have same i value: 
        if i != 4 and i != 8 and i  < 11:
            type_list: list = ['sword', 'wood', 'gold', 'cup']
            add_to_deck(type_list, card_num, i, envido_value, deck)
        # case weak 7s
        if i == 4:
            type_list: list = [ 'wood', 'cup']
            add_to_deck(type_list, card_num, i, envido_value, deck)
        if i == 8:
            type_list: list = [ 'gold', 'cup']
            add_to_deck(type_list, card_num, i, envido_value, deck)
        if i == 11:
            type_list: list = [ 'gold']
            add_to_deck(type_list, card_num, i, envido_value, deck)
        if i == 12:
            type_list: list = ['sword']
            add_to_deck(type_list, card_num, i, envido_value, deck)
        if i == 13:
            type_list: list = ['wood']
            add_to_deck(type_list, card_num, i, envido_value, deck)
        if i == 14:
            type_list: list = ['sword']
            add_to_deck(type_list, card_num, i, envido_value, deck)
        
       
    # for i in deck:
    #     print(f'Carta {i['name']} :  {i['card_ascii_art']} \n')
    
    return deck



        