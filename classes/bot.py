from random import randint
from classes.player_options import PlayerOptions
class Bot(PlayerOptions):
    '''Handle, with probability, the way the bot acts in the game using random.randint'''
    def __init__(self, cards, player_num, game_num, falta_envido_val):
        super().__init__(cards, player_num, game_num, falta_envido_val)
        self.SMART_ENVIDO: int = 22
        self.NEED_ENVIDO: int = 25
    

    def asks_envido(self, game_instance: int, envidos_calls_history: dict[str, int], bet_on_table: str):
        '''Evaluate if there are conditions to ask envido or not and depending on what has been asked upload the bet. 
        '''
        can_even_ask_envido: bool = self.is_hand or game_instance == 1 
        is_smart_to_ask: bool = self.total_envido > self.SMART_ENVIDO and self.total_envido < self.NEED_ENVIDO

        if not can_even_ask_envido: return 

        if not is_smart_to_ask:
            #The bot can lie, it can be a sutil or an absurd bet asked, depending on the probabilities.
            ask_porobability: int = randint(1, 100)
            if ask_porobability < 75: # 75% chances he'll not ask anything
                return
            elif ask_porobability < 94 and not (
                envidos_calls_history['envido'] < 2 or 
                envidos_calls_history['real_envido'] or 
                envidos_calls_history['falta_envido']):
                #TODO add return message, something like bet_on_table:str -> [envido, real_envido, falta_envido]
                envidos_calls_history['envido'] +=1
            elif ask_porobability < 97 and not (envidos_calls_history['real_envido'] or envidos_calls_history['falta_envido']):
                envidos_calls_history['real_envido']+=1

            else:
                envidos_calls_history['falta_envido'] = 1


        

