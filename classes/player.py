from classes.player_basics import PlayerBasics
from constants.types import *
class Player(PlayerBasics):
    def __init__(self, cards, player_num, game_num, falta_envido_val):
        super().__init__(cards, player_num, game_num, falta_envido_val)

    
   
    def __evaluate_envido_options_based_on_calls(self, envidos_calls_history: dict[str, int], bet_on_table: str) -> dict[int, str]:
        '''deletes envido item from res if it completed it`s total calls'''

        res: dict[int, str] = {
            0: self.PASS,
            1: self.ENVIDO,
            2: self.REAL_ENVIDO,
            3: self.FALTA_ENVDO,
        }
        if bet_on_table:
            del res[0]
        if envidos_calls_history[self.ENVIDO] == 2:
            del res[1]
        if envidos_calls_history[self.REAL_ENVIDO]:
            if 1 in res: del res[1]
            del res[2]
        if envidos_calls_history[self.FALTA_ENVDO]:
            if 1 in res: del res[1]
            if 2 in res: del res[2]
            del res[3]

        if bet_on_table: 
            res[4] = "accept"
            res[5] = "dont_accept"

        return res

        
    def __display_options(self, envido_options: dict[int, str]):
        '''Show in terminal the envido options
            TODO: Change to GUIs managment
        '''
        return int(
            input(f"PLAYER ENVIDO: {self.total_envido}. SELECT AN OPTION {envido_options}: " )
        )
        
    
    def ask_envido(self, envidos_calls_history: dict[str, int], bet_on_table: Bet):
        '''TODO Change to visual interface once it's finished the envido logic
            Now handle via terminal.
        '''
        
        #1st evaluate the envido options based on the calls history
        actual_envido_options: dict[int, str] = self.__evaluate_envido_options_based_on_calls(envidos_calls_history, bet_on_table)
        user_response:int = self.__display_options(actual_envido_options)
        if actual_envido_options[user_response] in envidos_calls_history:
            print(envidos_calls_history[actual_envido_options[user_response]])
            envidos_calls_history[actual_envido_options[user_response]] += 1
        return actual_envido_options[user_response]
    


    def _pop_selected_card(self, cards_options:dict[int, Card| Bet], card_key: int) -> Card | Bet:
        '''Returns a card or a bet'''
        for card in self.cards:
            if card['name'] == cards_options[card_key]:
                poped_card: Card = self.cards.pop(card_key)
                return poped_card['card_ascii_art']
        #if it doen't match then it is a bet
        return cards_options[card_key]

    # def play_card(self, game_num: int, envido_calls_history: dict[str, int], truco_calls_history: dict[str, int], bet_on_table:Bet):
    # def play_card(self, truco_calls_history: dict[str, int]):

    #     #    if  self._in_envido_game(envido_calls_history):
    #     prev_cards_len: int = len(self.cards)

    #     while prev_cards_len == len(self.cards):
    #         cards_options: dict[int, Card] = self._show_cards_options(truco_calls_history)
    #         user_response = int(
    #             input(f"SELECT AN OPTION: {cards_options} ")
    #         )
    #         if user_response in cards_options:
    #             card_or_bet_selected:  Card | Bet = self._pop_selected_card(cards_options, user_response)
    #             print(card_or_bet_selected)

    # def render_player_options(self, is_in_envido: bool, hand: int, truco_calls_history: dict[str, int], envidos_calls_history: dict[str, int], envido_bet:str) -> dict[int, str]:
        
    #     res: str | any = ''
    #     options:  dict[int, str] =  self._show_cards_options(truco_calls_history)
    #     if hand == 1:
    #         options[4] = 'envido_options'
    #     while not res:
    #         user_decision: int = int(input(
    #             f'Select an option: {options}'
    #         ))

    #         if user_decision == 4:
    #             envido_decision: str = self.ask_envido(envidos_calls_history, envido_bet)
    #             if envido_decision != self.PASS:
    #                 is_in_envido = True
    #                 res = envido_decision
    def ask_truco(self, truco_calls_history: dict[str, int], bet_on_table: Bet, hand: int ) -> Bet:
        truco_options: Options = {}
        truco_call_available: Options = self._calc_truco_option(truco_calls_history)
        if bet_on_table and hand == 1:
            truco_options = {
                0: truco_call_available, 1: self.ENVIDO ,2:self.ACCEPT, 3: self.DONT_ACCEPT
            }
        elif bet_on_table:
            truco_options = {
                0: truco_call_available, 1:self.ACCEPT, 2: self.DONT_ACCEPT
            }
        else:
            truco_options = {
                0: truco_call_available, 1: self.PASS
            }

        player_selection: int = int(
            input(f'SELECT AN OPTION: {truco_options}')
        )   
        res: Bet = truco_options[player_selection]
        if res in truco_calls_history: truco_calls_history[res] += 1
        return truco_options[player_selection]        

      
    def play_card(self, other_player_movement: Movement, hand: int, envido_calls_history: dict[str, int], truco_calls_history: dict[str, int]) -> Movement:
        # is_in_envido: bool = 
        #### RESPONSE PROPS #####
        # is_user_betting: bool = False
        # user_response: PlayerAction = '' 
        
        ###RES = {is_user_betting, user_response}###
        
        is_last_move_bet: bool = other_player_movement['is_bet']
        last_action: PlayerAction = other_player_movement['player_action']

        playing_envido: bool = is_last_move_bet and last_action in self.envido_points_values 

        if playing_envido:
            return { 'is_bet': True, 'player_action':self.ask_envido(envido_calls_history, last_action)}
        
        if is_last_move_bet and not playing_envido: # -> Then we are betting for truco. only options need to be *upper truco bet, accept or dont_accept
            truco_bet_selection: Bet = self.ask_truco(truco_calls_history, last_action, hand)
            if truco_bet_selection == self.ENVIDO:
                truco_bet_selection = self.ask_envido(envido_calls_history, '') #None bet on table related on envido
            return {'is_bet': True, 'player_action': truco_bet_selection }
        
        ## Not in bet action:
        player_options: Options = self._show_player_options(truco_calls_history, hand)
        player_selection: int = int(
            input(f"SELECT AN OPTION: {player_options} ")
        )
        user_response: PlayerAction = player_options[player_selection]

        if user_response in envido_calls_history:
            return {'is_bet': True, 'player_action': self.ask_envido(envido_calls_history, '')}
        
        if user_response in truco_calls_history:
            truco_calls_history[user_response] += 1
            return {'is_bet': True, 'player_action': user_response}
        
        #user_response is a card
        return {
            'is_bet': False,
            'player_action': self._throw_selected_card(player_selection)
        }
