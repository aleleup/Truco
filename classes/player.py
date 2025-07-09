from classes.player_basics import PlayerBasics

class Player(PlayerBasics):
    def __init__(self, cards, player_num, game_num, falta_envido_val):
        super().__init__(cards, player_num, game_num, falta_envido_val)

    
   
    def __evaluate_envido_options_based_on_calls(self, envidos_calls_history: dict[str, int], bet_on_table: str) -> dict[int, str]:
        '''deletes envido item from res if it completed it`s total calls'''

        res: dict[int, str] = {
            0:'',
            1: 'envido',
            2: 'real_envido',
            3: 'falta_envido',
        }
        if bet_on_table:
            del res[0]
        if envidos_calls_history['envido'] == 2:
            del res[1]
        if envidos_calls_history['real_envido']:
            if 1 in res: del res[1]
            del res[2]
        if envidos_calls_history['falta_envido']:
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
        
    
    def ask_envido(self, envidos_calls_history: dict[str, int], bet_on_table: str):
        '''TODO Change to visual interface once it's finished the envido logic
            Now handle via terminal.
        '''
        
        #1st evaluate the envido options based on the calls history
        actual_envido_options: dict[int, str] = self.__evaluate_envido_options_based_on_calls(envidos_calls_history, bet_on_table)
        user_response:int = self.__display_options(actual_envido_options)
        if actual_envido_options[user_response] in envidos_calls_history: #User selected [envido, real_envido, falta_envido] and not [accept, dont_accept]
            envidos_calls_history[actual_envido_options[user_response]] =+ 1
        return actual_envido_options[user_response]
