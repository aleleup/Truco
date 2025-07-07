class PlayerBasics:
    def __init__(self, cards: list[dict], player_num: int, game_num: int, falta_envido_val:int):
        self.points: int = 0
        self.cards = cards
        self.player_num = player_num
        self.game_num = game_num
        self.falta_envido_val = falta_envido_val
        self.total_envido: int = 0
        self.is_hand: bool =  True if game_num %2 == player_num else False    
        self.envido_points: dict[str, int] = {
            'envido': 2,
            'real_envido': 3,
            'falta_envido': falta_envido_val
        }
        self.truco_points : dict[str, int] = {
            'truco': 2,  ## Only truco available
            're_truco': 3,
            'vale_cuatro': 4
        }

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


    def ask_envido(self, game_instance: int, envidos_calls_history: dict[str, int], bet_on_table: str) -> str:
        pass


    def add_envido_points(self, bet_calls_history: dict[str, int]) -> None:
        if bet_calls_history['falta_envido']: 
            self.points += self.falta_envido_val
            return
        
        for bet in bet_calls_history:
            # print(self.envido_points, self.truco_points ,bet_calls_history, bet)
            self.points += self.envido_points[bet] * bet_calls_history[bet]

    def add_truco_points(self, bet_calls_history: dict[str, int]) -> None:
        for bet in bet_calls_history:
            self.points += self.truco_points[bet]  * bet_calls_history[bet]
