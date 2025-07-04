from player_basics import PlayerBasics

class Player(PlayerBasics):
    def __init__(self, cards, player_num, game_num, falta_envido_val):
        super().__init__(cards, player_num, game_num, falta_envido_val)

    
    def __eval_and_delet_prop(self, envidos_calls_history:dict[str, int], res:dict[int, str],  i:int, vlw:int ):
        if envidos_calls_history[res[i]] == vlw:
            del res[i]
    def __evaluate_envido_options_based_on_calls(self, envidos_calls_history: dict[str, int]) -> dict[int, str]:
        res: dict[int, str] = {
            0: 'envido',
            1: 'real_envido',
            2: 'falta_envido'
        }
        self.__evaluate_envido_options_based_on_calls(envidos_calls_history, res, 0, 2)
        self.__evaluate_envido_options_based_on_calls(envidos_calls_history, res, 1, 1)
        self.__evaluate_envido_options_based_on_calls(envidos_calls_history, res, 2, 2)

        
        
    
    def ask_envido(self, game_instance, envidos_calls_history, bet_on_table):
        '''TODO Change to visual interface once it's finished the envido logic
            Now handle via terminal.
        '''

        #1st evaluate the envido options based on the calls history