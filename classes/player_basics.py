from constants.types import *
class PlayerBasics:
    def __init__(self, cards: list[dict], player_num: int, game_num: int, falta_envido_val:int):
        self.points: int = 0
        self.cards: Deck = cards
        self.player_num: int = player_num
        self.game_num: int = game_num
        self.falta_envido_val: int = falta_envido_val
        self.total_envido: int = 0
        self.is_hand: bool =  True if game_num %2 == player_num else False    
        self.envido_points_values: dict[str, int] = {
            'envido': 2,
            'real_envido': 3,
            'falta_envido': falta_envido_val
        }
        #Envido key values (next to be used in GUIS)
        self.ENVIDO: str = 'envido'
        self.REAL_ENVIDO: str = 'real_envido'
        self.FALTA_ENVDO: str = 'falta_envido'

        #Truco key values:
        self.TRUCO: str = 'truco'
        self.RE_TRUCO: str = 're_truco'
        self.VALE_CUATRO: str = 'vale_cuatro'

        self.PASS: str = 'pass'
        self.ACCEPT: str = 'accept'
        self.DONT_ACCEPT: str = 'dont_accept'
        self.truco_points_values : dict[str, int] = {
            'truco': 2,  ## Only truco available
            're_truco': 3,
            'vale_cuatro': 4
        }

        # self.player_options: dict[int, str | int | dict[int | str]] = {
        #     0: cards,
        #     ''
        # }

    def print_cards(self) -> None:
        print(f'''
                ####### CARDS #######
                {self.cards[0]['name']} | {self.cards[1]['name']} | {self.cards[2]['name']}
    ''')

    def _pop_lowest_val(self, l:list, prop:str) -> None:
        index: int = 0
        comp: int = 0
        for i in range(len(l)):
            if i == 0:
                comp = l[i][prop]
            if l[i][prop] < comp:
                index = i
                comp = l[i][prop]
        l.pop(index)

    def _pop_highest_card(self, cards: Deck) -> None:
        index: int = 0
        comp: int = 0
        for i in range(len(cards)):
            if cards[i]['value'] > comp:
                index = i
                comp = cards[i]['value']
        cards.pop(index)

    def _cards_deep_copy(self) -> Deck:
        cards_copy: Deck = []
        for card in self.cards:
            card_copy = card.copy()
            cards_copy.append(card_copy)
        return cards_copy

    def calc_envido(self) -> int:
        '''Each player calculates their own envidos'''
        total_envido: int = 0
        max_envido_val: int = 0
        same_type_list: list[dict[str, str| int]] = []
        i: int = 0
        while i < 3:
            # while it's not assure that i'll have more than one card of same type, return value updates to the max envido_value
            if self.cards[i]['envido_value'] > total_envido: total_envido = self.cards[i]['envido_value']
            j: int = i+1
            while j < len(self.cards):
                if self.cards[i]['type'] == self.cards[j]['type']:
                    if self.cards[i] not in same_type_list: same_type_list.append(self.cards[i])
                    if self.cards[j] not in same_type_list: same_type_list.append(self.cards[j])
                j+=1
            i+=1
        if same_type_list:
            if len(same_type_list) == len(self.cards):
                self._pop_lowest_val(same_type_list, 'envido_value')
            total_envido = 0
            for card in same_type_list:
                total_envido += card['envido_value']
            total_envido+= 20 
        self.total_envido = total_envido


    def ask_envido(self, envidos_calls_history: dict[str, int], bet_on_table: Bet) -> Bet:
        pass
    
    def ask_truco(self, truco_calls_history: dict[str, int], bet_on_table: Bet, hand: int) -> Bet:
        pass
    
    def add_unwanted_envido_points(self, envido_calls_history: dict[str, int])-> None:
        print(f'envido_points to add: {envido_calls_history}')
        for key in envido_calls_history:
            if envido_calls_history[key]: 
                self.points += envido_calls_history[key]
    
    def add_envido_points(self, bet_calls_history: dict[str, int]) -> None:
        if bet_calls_history['falta_envido']: 
            self.points += self.falta_envido_val
            return
        
        for bet in bet_calls_history:
            # print(self.envido_points, self.truco_points ,bet_calls_history, bet)
            self.points += self.envido_points_values[bet] * bet_calls_history[bet]

    def add_truco_points(self, bet_calls_history: dict[str, int]) -> None:
        for bet in bet_calls_history:
            self.points += self.truco_points_values[bet]  * bet_calls_history[bet]

    def _truco_available_based_on_history(self, truco_calls_history: dict[str,int])-> Bet:
        if not truco_calls_history[self.TRUCO]:
            return self.TRUCO
        if truco_calls_history[self.TRUCO] and not truco_calls_history[self.RE_TRUCO]:
            return self.RE_TRUCO
        if truco_calls_history[self.RE_TRUCO] and not truco_calls_history[self.VALE_CUATRO]:
            return self.VALE_CUATRO 
    
    def _calculate_truco_options(self, truco_calls_history: dict[str, int], bet_on_table:Bet, hand: int) -> Options:
        truco_call_available: Bet = self._truco_available_based_on_history(truco_calls_history)
        if bet_on_table and hand == 1:
            return {
                0: truco_call_available, 1: self.ENVIDO ,2:self.ACCEPT, 3: self.DONT_ACCEPT
            }
        elif bet_on_table:
            return {
                0: truco_call_available, 1:self.ACCEPT, 2: self.DONT_ACCEPT
            }
        else:
            return {
                0: truco_call_available, 1: self.PASS
            }

    
    def _show_player_options(self, truco_calls_history: dict[str,int], hand: int) -> Options | None:
        '''returns options based on is_bet and if last player_action is not in envido_calls. 
            return null if is in envido.'''
        res: Options = {}
        key: int = 0
        for card in self.cards:
            res[key] = card['name'] 
            key+=1
        if hand == 1: 
            res[key] = self.ENVIDO
            res[key+1] = self._truco_available_based_on_history(truco_calls_history)
        else:
            res[key] = self._truco_available_based_on_history(truco_calls_history)
        return res   
                
    def _throw_selected_card(self, i: int) -> Card:
        '''pop the i index card of cards'''
        return self.cards.pop(i)
        
    def play_card(self, other_player_movement: Movement, hand: int, envido_calls_history: dict[str, int], truco_calls_history: dict[str, int]) -> Movement:
        '''Player throw's cards on the table.
        TODO: integrate play_cards with envido on first hand.
        '''
        