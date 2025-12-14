from classes.Card import Card
from constants.types import *
class Player():
    def __init__(self, id: int) -> None:
        self._cards: list[Card] = []
        self._points: int = 0
        self._total_envido: int = 0
        self._id: int = id
        self._options: PlayerOptions = {}
        self._is_player_turn: bool = False
        
    def _show_cards(self) -> list[dict[str, str | int]]: 
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
        if self._points > 30: self.points = 30


    def status(self) -> PlayerStatus:
        return {
            "player_id": self._id,
            "points": self._points,
            "cards": self._show_cards(),
            "options": self._options,
            "envido": self._total_envido,
            "is_player_turn": self._is_player_turn
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
        self._total_envido = total_envido

    def get_envido(self) -> int:
        return self._total_envido
#--------------------------------------------------
  
    def remove_card(self, i:int) -> Card:
        print(self._cards)
        return self._cards.pop(i)
    
    def set_options(self, options: PlayerOptions) -> None:
        self._options = options

    def get_points(self) -> int: return self._points

    def toggle_turn(self) -> None: self._is_player_turn = not self._is_player_turn