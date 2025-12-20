from constants.emojis import * 
from constants.types import *
from classes.Card import Card
from random import randint
class TrucoDeck:
    def __init__(self) -> None:
        self.cards: list[Card] = []
        
    def _calc_card_num(self, i: int) -> int:
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
        return 0

    def _calc_envido_value(self, card_num: int) -> int:
        if card_num in [12, 11, 10]:
            return 0
        return card_num   

    def _add_to_deck(self, type_list: list[str], card_num:int, card_value: int, envido_value: int):
        for type in type_list:
            new_card: Card = Card(card_num, type, card_value, envido_value)
            self.cards.append(new_card)

    def create_deck(self) -> None:
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
        for i in range(1, 15):
            card_num: int = self._calc_card_num(i)
            envido_value: int = self._calc_envido_value(card_num)
            # case all cards num have same i value: 
            if i != 4 and i != 8 and i  < 11:
                type_list: list[str] = ['sword', 'wood', 'gold', 'cup']
                self._add_to_deck(type_list, card_num, i, envido_value)
            # case weak 7s
            if i == 4:
                type_list: list[str] = [ 'wood', 'cup']
                self._add_to_deck(type_list, card_num, i, envido_value)
            if i == 8:
                type_list: list[str] = [ 'gold', 'cup']
                self._add_to_deck(type_list, card_num, i, envido_value)
            if i == 11:
                type_list: list[str] = [ 'gold']
                self._add_to_deck(type_list, card_num, i, envido_value)
            if i == 12:
                type_list: list[str] = ['sword']
                self._add_to_deck(type_list, card_num, i, envido_value)
            if i == 13:
                type_list: list[str] = ['wood']
                self._add_to_deck(type_list, card_num, i, envido_value)
            if i == 14:
                type_list: list[str] = ['sword']
                self._add_to_deck(type_list, card_num, i, envido_value)
            
    def shuffle_cards(self) -> list[list[Card]]:
        '''Returns 2 lists of 3 diferent cards'''
        print("CARDS ", len(self.cards))
        hand_player_cards: list[Card] = []
        foot_player_cards: list[Card] = []

        response: list[list[Card]] = [hand_player_cards, foot_player_cards]
        cards_index_in_use: list[int] = []
        for players_card in response:
            i: int = 0
            while i < 3:
                card_index: int = randint(0, len(self.cards) - 1)
                if card_index not in cards_index_in_use:
                    cards_index_in_use.append(i)
                    players_card.append(self.cards[card_index])
                    i+=1

        return response


            