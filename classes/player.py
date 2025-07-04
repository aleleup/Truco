from classes.player_basics import PlayerBasics

class Player(PlayerBasics):
    def __init__(self, cards, player_num, game_num, falta_envido_val):
        super().__init__(cards, player_num, game_num, falta_envido_val)

    
    def __eval_and_delet_prop(self, envidos_calls_history:dict[str, int], res:dict[int, str],  i:int, vlw:int ):
        '''deletes item from res depending on it;s value'''
        if envidos_calls_history[res[i]] == vlw:
            del res[i]
    def __evaluate_envido_options_based_on_calls(self, envidos_calls_history: dict[str, int], bet_on_table: str) -> dict[int, str]:
        '''deletes envido item from res if it completed it`s total calls'''

        res: dict[int, str] = {
            0:'',
            1: 'envido',
            2: 'real_envido',
            3: 'falta_envido',
        }
        self.__eval_and_delet_prop(envidos_calls_history, res, 1, 2)
        self.__eval_and_delet_prop(envidos_calls_history, res, 2, 1)
        self.__eval_and_delet_prop(envidos_calls_history, res, 3, 2)
    
        if bet_on_table: 
            res[3] = "accept"
            res[4] = "dont_accept"

        return res

        
    def __display_options(self, envido_options: dict[int, str]):
        '''Show in terminal the envido options
            TODO: Change to GUIs managment
        '''
        return int(
            input(f"SELECT AN OPTION {envido_options}" )
        )
        
    
    def ask_envido(self, game_instance, envidos_calls_history, bet_on_table):
        '''TODO Change to visual interface once it's finished the envido logic
            Now handle via terminal.
        '''
        if game_instance != 1: return
        #1st evaluate the envido options based on the calls history
        actual_envido_options: dict[int, str] = self.__evaluate_envido_options_based_on_calls(envidos_calls_history, bet_on_table)
        user_response:int = self.__display_options(actual_envido_options)
        return actual_envido_options[user_response]