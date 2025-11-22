from classes.Card import Card
from constants.types import *
class Player():
    def __init__(self, id: int) -> None:
        self._cards: list[Card]
        self._points: int = 0
        self.total_envido: int = 0
        self.id: int = id
    def show_card(self) -> list[dict[str, str | int]]: 
        res: list[dict[str, str | int]] = []
        for card in self._cards:
            card_data: dict[str, str | int] = {
                'name': card.name,
                'value': card.value,
                'type': card.type,
                'envido_value': card.envido_value
            }
            res.append(card_data)
        return res
    

    def set_cards(self, cards: list[Card]) -> None:
        self._cards = cards
        self._calc_envido()

    def add_points(self, points: int):
        self._points += points


    def show_player_data(self) -> PlayerStatus:
        return {
            "player_id": self.id,
            "points": self._points,
            "cards": self.show_card(),
            "envido": self.total_envido
        }
    
    # --------ENVIDO METHODS----------
    def _pop_lowest_envido_val(self, l:list[Card]) -> None:
        index: int = 0
        comp: int = 0
        for i in range(len(l)):
            if i == 0:
                comp = l[i].envido_value
            if l[i].envido_value < comp:
                index = i
                comp = l[i].envido_value
        l.pop(index)
    def _calc_envido(self) -> None:
        '''Each player calculates their own envidos'''
        total_envido: int = 0
        # max_envido_val: int = 0
        same_type_list: list[Card] = []
        i: int = 0
        while i < 3:
            # while it's not assure that i'll have more than one card of same type, return value updates to the max envido_value
            if self._cards[i].envido_value > total_envido: total_envido = self._cards[i].envido_value
            j: int = i+1
            while j < len(self._cards):
                if self._cards[i].type == self._cards[j].type:
                    if self._cards[i] not in same_type_list: same_type_list.append(self._cards[i])
                    if self._cards[j] not in same_type_list: same_type_list.append(self._cards[j])
                j+=1
            i+=1
        if same_type_list:
            if len(same_type_list) == len(self._cards):
                self._pop_lowest_envido_val(same_type_list )
            total_envido = 0
            for card in same_type_list:
                total_envido += card.envido_value
            total_envido+= 20 
        self.total_envido = total_envido
#--------------------------------------------------
  
