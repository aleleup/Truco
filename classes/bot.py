from random import randint
from classes.player_basics import PlayerBasics
from constants.types import *
class Bot(PlayerBasics):
    '''Handle, with probability, the way the bot acts in the game using random.randint'''
    def __init__(self, cards, player_num, game_num, falta_envido_val):
        super().__init__(cards, player_num, game_num, falta_envido_val)
        self.SMART_ENVIDO: int = 22
        self.NEED_ENVIDO: int = 27
        self.playing_envido:bool = False
        self.playing_truco:bool = False

        self.EXCELENT_TRUCO: int = 11
        self.GOOD_TRUCO: int = 9
        self.ACCEPTABLE_TRUCO: int = 7
        self.BAD_TRUCO: int = 5
        self.HORRIBLE_TRUCO: int = 1

        self.truco_status: str = ''

    def _create_key_or_add_to_property(self, cards_status_counter: dict[str, int], property: str) -> None:
        if property in cards_status_counter:
            cards_status_counter[property] += 1
        else:
            cards_status_counter[property] = 1

    def _define_hand_status(self) -> None:
        '''Stablish if hand is good or bad'''
        # cards_copy = self._cards_deep_copy(self.cards)
        cards_status_counter: dict[str, int] = {}
        for card_to_analize in self.cards:
            if card_to_analize['value'] >= self.EXCELENT_TRUCO:
                self._create_key_or_add_to_property(cards_status_counter, 'EXCELLENT')

            if card_to_analize['value'] < self.EXCELENT_TRUCO and card_to_analize['value'] >= self.GOOD_TRUCO:
                self._create_key_or_add_to_property(cards_status_counter, 'GOOD')

            if card_to_analize['value'] < self.GOOD_TRUCO and card_to_analize['value'] >= self.ACCEPTABLE_TRUCO:
                self._create_key_or_add_to_property(cards_status_counter, 'ACCEPTABLE')

            if card_to_analize['value'] < self.ACCEPTABLE_TRUCO and card_to_analize['value'] >= self.BAD_TRUCO:
                self._create_key_or_add_to_property(cards_status_counter, 'BAD')

            if card_to_analize['value'] < self.BAD_TRUCO and card_to_analize['value'] >= self.HORRIBLE_TRUCO:
                self._create_key_or_add_to_property(cards_status_counter, 'HORRIBLE')

        return cards_status_counter

                

    
    def __handle_not_smart_to_envido(self, envidos_calls_history: dict[str, int]) -> str:
        '''Depending on the ask_probability the bot ask whitch envido will select to lie'''
        ask_probability: int = randint(1, 100)
        # print("ASKING PROBABILITY BAD ENVIDO", ask_probability)
        
        if self.playing_envido: return self.DONT_ACCEPT

        if ask_probability <= 75 and not self.playing_envido: return self.PASS

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
        if self.playing_envido:
            if self.total_envido >= 25: return self.ACCEPT
            return self.DONT_ACCEPT
        envido_calls_history[self.ENVIDO] +=1
        return self.ENVIDO
    
    def __handle_grate_envido(self,envido_calls_history: dict[str, int]) -> str:
        '''Based on points and probabilities, the bot will ask a great bet, go fishing or keep it safe'''
        ask_probability: int = randint(1,100)
        # print("ASKING PROBABILITY GREAT ENVIDO", ask_probability)

        if ask_probability > 80 and not (self.playing_envido or self.playing_truco):
           
            return self.PASS 
        
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
        

        if not (is_smart_to_ask or is_grate_envido):
            #The bot can lie, it can be a sutil or an absurd bet asked, depending on the probabilities.
            return self.__handle_not_smart_to_envido( envidos_calls_history)
        if is_smart_to_ask:
            return self.__handle_smart_envido(envidos_calls_history)
        if is_grate_envido:
            return self.__handle_grate_envido(envidos_calls_history)
    

    def _handle_truco_calls(cards_status: dict[str, int], truco_calls_history: dict[str, int]) -> Bet:
        '''responses or starts a truco bet'''
        #TODO implement this function
    
    def ask_truco(self, truco_calls_history: dict[str, int], envido_calls_history: dict[str, int] ,bet_on_table: Bet, hand: int) -> Bet:
        truco_available_options: Options = self._calculate_truco_options(truco_calls_history, bet_on_table, hand)
        cards_status: dict[str, int] = self._define_hand_status()
        bot_action: Bet = ''
        print(f"BOT TRUCO OPTION {truco_available_options} && CARDS STATUS {cards_status}")
        if self.ENVIDO in truco_available_options:
            bot_action = self.ask_envido(envido_calls_history, bet_on_table)
        if bot_action != self.PASS: return bot_action

        #"else"
        return self._handle_truco_calls(cards_status, truco_calls_history)
         
        

            


    def play_card(self, other_player_movement: Movement, hand: int, envido_calls_history: dict[str, int], truco_calls_history: dict[str, int]) -> Movement:
        is_last_move_bet: bool = other_player_movement['is_bet']
        last_action: PlayerAction = other_player_movement['player_action']
        self.playing_envido = last_action in envido_calls_history and is_last_move_bet
        self.playing_truco = last_action in truco_calls_history and is_last_move_bet

        # bot_action: PlayerAction = ''
        if self.playing_envido:
            return { 'is_bet': True, 'player_action':self.ask_envido(envido_calls_history, last_action)}
        
        elif self.playing_truco: 
            truco_bet_selection: Bet = self.ask_truco(truco_calls_history, envido_calls_history, last_action, hand)
            return {'is_bet': True, 'player_action': truco_bet_selection }
        
