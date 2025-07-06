from random import randint
from classes.player_basics import PlayerBasics
class Bot(PlayerBasics):
    '''Handle, with probability, the way the bot acts in the game using random.randint'''
    def __init__(self, cards, player_num, game_num, falta_envido_val):
        super().__init__(cards, player_num, game_num, falta_envido_val)
        self.SMART_ENVIDO: int = 22
        self.NEED_ENVIDO: int = 27
        self.ENVIDO: str = 'envido'
        self.REAL_ENVIDO: str = 'real_envido'
        self.FALTA_ENVDO: str = 'falta_envido'
        self.ACCEPT: str = 'accept'
        self.DONT_ACCEPT: str = 'dont_accept'
        self.is_bet_on_table:bool = False
        
    def __handle_not_smart_to_envido(self, envidos_calls_history: dict[str, int]) -> str:
        '''Depending on the ask_probability the bot ask whitch envido will select to lie'''
        ask_probability: int = randint(1, 100)
        # print("ASKING PROBABILITY BAD ENVIDO", ask_probability)
        
        if self.is_bet_on_table: return self.DONT_ACCEPT


        if ask_probability <= 75: return ''

        if ask_probability < 94 and not (
            envidos_calls_history['envido'] < 2 or envidos_calls_history['real_envido'] or envidos_calls_history['falta_envido']
        ):
            envidos_calls_history['envido'] +=1
            return self.ENVIDO
        elif ask_probability < 98 and not (
            envidos_calls_history['real_envido'] or envidos_calls_history['falta_envido']
        ):
            envidos_calls_history['real_envido']+=1
            return self.REAL_ENVIDO
        else:
            envidos_calls_history['falta_envido'] = 1
            return self.FALTA_ENVDO

    def __handle_smart_envido(self,envido_calls_history: dict[str, int]) -> str:
        '''Keep it safe... for now'''
        if self.is_bet_on_table:
            if self.total_envido >= 25: return self.ACCEPT
            return self.DONT_ACCEPT
        envido_calls_history['envido'] +=1
        return self.ENVIDO
    
    def __handle_grate_envido(self,envido_calls_history: dict[str, int]) -> str:
        '''Based on points and probabilities, the bot will ask a great bet, go fishing or keep it safe'''
        ask_probability: int = randint(1,100)
        # print("ASKING PROBABILITY GREAT ENVIDO", ask_probability)

        if ask_probability > 80 and not (self.is_bet_on_table):
            # print("GOES FISHING")
            return '' 
        
        if envido_calls_history['envido'] == 1 and (self.total_envido < 30 or ask_probability <= 33):
            #33% chances of asking envido once it has been called
            envido_calls_history['envido'] +=1
            return self.ENVIDO
        if not(envido_calls_history['real_envido']) and (self.total_envido < 32 or ask_probability <= 66):
            # 33% chances of asking real_envido (doesn't matter what's the actual bet)
            envido_calls_history['real_envido'] += 1
            return self.REAL_ENVIDO
        
        if not(envido_calls_history['falta_envido']) and ask_probability <= 80: ## has envido >= 32
            envido_calls_history['falta_envido'] +=1
            return self.FALTA_ENVDO
        
        ##Handler to keep it safe
        envido_calls_history['envido'] +=1
        return self.ENVIDO

        

    def ask_envido(self, game_instance: int, envidos_calls_history: dict[str, int], bet_on_table: str):
        '''Evaluate if there are conditions to ask envido or not and depending on what has been asked upload the bet.'''
        can_even_ask_envido: bool = game_instance == 1 
        is_smart_to_ask: bool = self.total_envido >= self.SMART_ENVIDO and self.total_envido < self.NEED_ENVIDO
        is_grate_envido: bool = self.total_envido >= self.NEED_ENVIDO
        self.is_bet_on_table = bool(bet_on_table)
        print(self.is_bet_on_table)
        if not can_even_ask_envido: return 

        if not (is_smart_to_ask or is_grate_envido):
            #The bot can lie, it can be a sutil or an absurd bet asked, depending on the probabilities.
            return self.__handle_not_smart_to_envido( envidos_calls_history)
        if is_smart_to_ask:
            return self.__handle_smart_envido(envidos_calls_history)
        if is_grate_envido:
            return self.__handle_grate_envido(envidos_calls_history)
        

