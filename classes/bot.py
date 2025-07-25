from random import randint
from classes.player_basics import PlayerBasics
from constants.types import *
class Bot(PlayerBasics):
    '''Handle, with probability, the way the bot acts in the game using random.randint'''
    def __init__(self, cards, player_num, game_num, falta_envido_val):
        super().__init__(cards, player_num, game_num, falta_envido_val)
        self.SMART_ENVIDO: int = 22
        self.NEED_ENVIDO: int = 27
        self.is_bet_on_table:bool = False
        
        self.is_excelent_truco: bool # avarage(truco_logic_values) > x (x:int) 
        self.is_acceptable_truco: bool # y <= avarage(truco_logic_values) < x (x:int, y:int) 
        self.is_bad_truco: bool # y > avarage(truco_logic_values)


    
    def __handle_not_smart_to_envido(self, envidos_calls_history: dict[str, int]) -> str:
        '''Depending on the ask_probability the bot ask whitch envido will select to lie'''
        ask_probability: int = randint(1, 100)
        # print("ASKING PROBABILITY BAD ENVIDO", ask_probability)
        
        if self.is_bet_on_table: return self.DONT_ACCEPT

        if ask_probability <= 75 and not self.is_bet_on_table: return self.PASS

        if ask_probability < 94 and not (
            envidos_calls_history[self.ENVIDO] < 2 or envidos_calls_history[self.REAL_ENVIDO] or envidos_calls_history[self.FALTA_ENVDO]
        ):
            envidos_calls_history[self.ENVIDO] +=1
            return self.ENVIDO
        elif ask_probability < 98 and not (
            envidos_calls_history[self.REAL_ENVIDO] or envidos_calls_history[self.FALTA_ENVDO]
        ):
            envidos_calls_history[self.REAL_ENVIDO]+=1
            return self.REAL_ENVIDO
        else:
            envidos_calls_history[self.FALTA_ENVDO] = 1
            return self.FALTA_ENVDO

    def __handle_smart_envido(self,envido_calls_history: dict[str, int]) -> str:
        '''Keep it safe... for now'''
        if self.is_bet_on_table:
            if self.total_envido >= 25: return self.ACCEPT
            return self.DONT_ACCEPT
        envido_calls_history[self.ENVIDO] +=1
        return self.ENVIDO
    
    def __handle_grate_envido(self,envido_calls_history: dict[str, int]) -> str:
        '''Based on points and probabilities, the bot will ask a great bet, go fishing or keep it safe'''
        ask_probability: int = randint(1,100)
        # print("ASKING PROBABILITY GREAT ENVIDO", ask_probability)

        if ask_probability > 80 and not (self.is_bet_on_table):
            # print("GOES FISHING")
            return None 
        
        if envido_calls_history[self.ENVIDO] == 1 and not (
        envido_calls_history[self.REAL_ENVIDO] or envido_calls_history[self.REAL_ENVIDO]
        ) and (
            self.total_envido < 30 or ask_probability <= 33
        ):
            #33% chances of asking envido once it has been called
            envido_calls_history[self.ENVIDO] +=1
            return self.ENVIDO
        if not(envido_calls_history[self.REAL_ENVIDO]) and (self.total_envido < 32 or ask_probability <= 66):
            # 33% chances of asking real_envido (doesn't matter what's the actual bet)
            envido_calls_history[self.REAL_ENVIDO] += 1
            return self.REAL_ENVIDO
        
        if not(envido_calls_history[self.REAL_ENVIDO]) and ask_probability <= 80: ## has envido >= 32
            envido_calls_history[self.FALTA_ENVDO] +=1
            return self.FALTA_ENVDO
        
        ##Handler to keep it safe
        envido_calls_history[self.ENVIDO] +=1
        return self.ENVIDO

    def ask_envido(self, envidos_calls_history: dict[str, int], bet_on_table: Bet) -> Bet:
        '''Evaluate if there are conditions to ask envido or not and depending on what has been asked upload the bet.'''
        is_smart_to_ask: bool = self.total_envido >= self.SMART_ENVIDO and self.total_envido < self.NEED_ENVIDO
        is_grate_envido: bool = self.total_envido >= self.NEED_ENVIDO
        self.is_bet_on_table = False if bet_on_table == self.PASS else bool(bet_on_table)
        

        if not (is_smart_to_ask or is_grate_envido):
            #The bot can lie, it can be a sutil or an absurd bet asked, depending on the probabilities.
            return self.__handle_not_smart_to_envido( envidos_calls_history)
        if is_smart_to_ask:
            return self.__handle_smart_envido(envidos_calls_history)
        if is_grate_envido:
            return self.__handle_grate_envido(envidos_calls_history)
    
    def ask_truco(self, truco_calls_history: dict[str, int], bet_on_table: Bet, hand: int) -> Bet:
        truco_available_options: Options = self._calculate_truco_options(truco_calls_history, bet_on_table, hand)



    def play_card(self, other_player_movement: Movement, hand: int, envido_calls_history: dict[str, int], truco_calls_history: dict[str, int]) -> Movement:
        is_last_move_bet: bool = other_player_movement['is_bet']
        last_action: PlayerAction = other_player_movement['player_action']

        playing_envido: bool = is_last_move_bet and last_action in envido_calls_history

        if playing_envido:
            #TODO -> change logic so bot can go fishing
            return { 'is_bet': True, 'player_action':self.ask_envido(envido_calls_history, last_action)}
        
        if is_last_move_bet and not playing_envido: # -> Then we are betting for truco. only options need to be *upper truco bet, accept or dont_accept
            truco_bet_selection: Bet = self.ask_truco(truco_calls_history, last_action, hand)
            if truco_bet_selection == self.ENVIDO:
                truco_bet_selection = self.ask_envido(envido_calls_history, '') #None bet on table related on envido
            return {'is_bet': True, 'player_action': truco_bet_selection }
        
