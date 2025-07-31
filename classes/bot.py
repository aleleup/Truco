from random import randint
from classes.player_basics import PlayerBasics
from constants.types import *
class Bot(PlayerBasics):
    '''Handle, with probability, the way the bot acts in the game using random.randint'''
    '''Sometimes, Bot lies in envido. This bot becomes more risky when he is winning, he takes confidence'''
    '''Maybe, some day I can make diferent bots with diferents params'''
    def __init__(self, cards, player_num, game_num, falta_envido_val):
        super().__init__(cards, player_num, game_num, falta_envido_val)
        self.SMART_ENVIDO: int = 22
        self.NEED_ENVIDO: int = 27
        self.playing_envido:bool = False
        self.playing_truco:bool = False

        self.EXCELLENT_TRUCO: int = 11
        self.GOOD_TRUCO: int = 9
        self.ACCEPTABLE_TRUCO: int = 5
        self.BAD_TRUCO: int = 1
        # self.HORRIBLE_TRUCO: int = 1

        self.winning: bool = False

    ######### START OF LOGIC AUX FUNCTIONS #########   

    def _create_key_or_add_to_property(self, cards_status_counter: dict[str, int], property: str) -> None:
        if property in cards_status_counter:
            cards_status_counter[property] += 1
        else:
            cards_status_counter[property] = 1

    def _define_hand_status(self) -> None:
        '''Stablish if hand is good or bad'''
        # cards_copy = self._cards_deep_copy(self.cards)
        cards_status_counter: dict[str, int] = {
            'EXCELLENT': 0,
            'GOOD': 0,
            'ACCEPTABLE': 0,
            'BAD': 0,
        }
        for card_to_analize in self.cards:
            if card_to_analize['value'] >= self.EXCELLENT_TRUCO:
                cards_status_counter['EXCELLENT'] +=1 

            if card_to_analize['value'] < self.EXCELLENT_TRUCO and card_to_analize['value'] >= self.GOOD_TRUCO:
                cards_status_counter['GOOD'] +=1 

            if card_to_analize['value'] < self.GOOD_TRUCO and card_to_analize['value'] >= self.ACCEPTABLE_TRUCO:
                cards_status_counter['ACCEPTABLE'] +=1 

            if card_to_analize['value'] < self.ACCEPTABLE_TRUCO and card_to_analize['value'] >= self.BAD_TRUCO:
                cards_status_counter['BAD'] +=1

            # if card_to_analize['value'] < self.BAD_TRUCO and card_to_analize['value'] >= self.HORRIBLE_TRUCO:
            #     cards_status_counter['HORRIBLE'] +=1 
        return cards_status_counter

    ######### END OF LOGIC AUX FUNCTIONS #########   

    ######### START OF ENVIDO FUNCTIONS #########   
    
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
        
     ######### END OF ENVIDO FUNCTIONS #########   

     ######### START OF TRUCO FUNCTIONS #########   
    
    def _return_pass_or_dont_accept(self) -> Bet:
        if self.playing_truco: return self.DONT_ACCEPT
        else:
            return self.PASS

    def _return_upgrade_of_truco_bet(self, truco_upgrade_option: Bet, truco_calls_history: dict[str, int]) -> Bet:
        if truco_upgrade_option:
            truco_calls_history[truco_upgrade_option] +=1
            return truco_upgrade_option
        
        else:
            if self.playing_truco: return self.ACCEPT
            return self.PASS

    
    def _handle_first_hand_truco_call(self, cards_status: dict[str, int], truco_calls_history: dict[str, int], truco_upgrade_option: Bet) -> Bet:
        '''To consoder: cards in hand == 3'''
         ###WHEN TO UPGRADE THE BET
        excelent_cards_amount: int = cards_status.get('EXCELLENT')
        good_cards_amount: int = cards_status.get('GOOD')
        acceptable_cards_amount: int = cards_status.get('ACCEPTABLE')
        if (
            (good_cards_amount and good_cards_amount <= 2 and excelent_cards_amount == 1) or 
            (good_cards_amount == 1 and excelent_cards_amount and excelent_cards_amount <= 2) or 
            good_cards_amount == 3 or excelent_cards_amount == 3
            ):
            if self.playing_truco:
                return self._return_upgrade_of_truco_bet(truco_upgrade_option, truco_calls_history)
            else:
                return self.PASS

         ###WHEN TO ACCEPT
        if  ((good_cards_amount or excelent_cards_amount) and acceptable_cards_amount >= 1) or good_cards_amount >= 2 or excelent_cards_amount >= 2:            
            if self.playing_truco:
                return self.ACCEPT
            else:
                return self.PASS

        ###WHEN TO CONSIDER
        if not (good_cards_amount or excelent_cards_amount) and acceptable_cards_amount >= 2:
            random_num: int = randint(0, 100)
            if self.playing_truco and random_num >= 65: 
                return self.ACCEPT
            return self._return_pass_or_dont_accept()
        # ELSE (HANDLER)
        return self._return_pass_or_dont_accept()
    
    def _handle_second_hand_truco_call(self, cards_status: dict[str, int], truco_calls_history: dict[str, int], truco_upgrade_option: Bet) -> Bet:
         ###WHEN TO UPGRADE THE BET 
        excelent_cards_amount: int = cards_status.get('EXCELLENT')
        good_cards_amount: int = cards_status.get('GOOD')
        acceptable_cards_amount: int = cards_status.get('ACCEPTABLE')
        if (good_cards_amount and excelent_cards_amount) or good_cards_amount == 2 or excelent_cards_amount == 2:
            return self._return_upgrade_of_truco_bet(truco_upgrade_option, truco_calls_history)

         ###WHEN TO ACCEPT
        if  ((good_cards_amount or excelent_cards_amount) and acceptable_cards_amount == 1 ):            
            if self.playing_truco:
                return self.ACCEPT
            else:
                return self._return_upgrade_of_truco_bet(truco_upgrade_option, truco_calls_history)

        ###WHEN TO CONSIDER
        if acceptable_cards_amount == 2:
            random_num: int = randint(0, 100)
            if self.playing_truco and random_num >= 75: 
                return self.ACCEPT
            return self._return_pass_or_dont_accept()

        # ELSE (HANDLER)
        return self._return_pass_or_dont_accept()
    
    def _handle_third_hand_truco_call(self, cards_status: dict[str, int], truco_calls_history: dict[str, int], truco_upgrade_option: Bet) -> Bet:
         ###WHEN TO UPGRADE THE BET 
        excelent_cards_amount: int = cards_status.get('EXCELLENT')
        good_cards_amount: int = cards_status.get('GOOD')
        acceptable_cards_amount: int = cards_status.get('ACCEPTABLE')
        bad_cards_amount: int = cards_status.get('BAD')
        if (good_cards_amount or excelent_cards_amount):
            return self._return_upgrade_of_truco_bet(truco_upgrade_option, truco_calls_history)

         ###WHEN TO ACCEPT
        if acceptable_cards_amount:            
            if self.playing_truco and not (truco_calls_history[self.RE_TRUCO] or truco_calls_history[self.VALE_CUATRO]):
                return self.ACCEPT
            else:
                return self._return_upgrade_of_truco_bet(truco_upgrade_option, truco_calls_history)

        ###WHEN TO CONSIDER
        if bad_cards_amount:
            random_num: int = randint(0, 100)
            if not self.playing_truco and random_num >= 75: 
                return self._return_upgrade_of_truco_bet(truco_upgrade_option, truco_calls_history)
            return self._return_pass_or_dont_accept()

        # ELSE (HANDLER)
        return self._return_pass_or_dont_accept()

    def _handle_truco_calls(self, cards_status: dict[str, int], truco_calls_history: dict[str, int], available_truco_option: Bet, hand:int) -> Bet:
        '''responses or starts a truco bet. On each hand ask if is good idea to ask truco based on statu, history, options and WHEN can the bot pass the oportunity and when it has to decide'''
        #WHEN to PASS ->
        if hand == 1:
            return self._handle_first_hand_truco_call(cards_status, truco_calls_history, available_truco_option)
        if hand == 2:
            return self._handle_second_hand_truco_call(cards_status, truco_calls_history, available_truco_option)
        if hand == 3:
            return self._handle_third_hand_truco_call(cards_status, truco_calls_history, available_truco_option)
       
       

    def ask_truco(self, truco_calls_history: dict[str, int], envido_calls_history: dict[str, int], bet_on_table: Bet, hand: int) -> Bet:
        truco_available_options: Options = self._calculate_truco_options(truco_calls_history, bet_on_table, hand)
        cards_status: dict[str, int] = self._define_hand_status()
        bot_action: Bet = ''
        print(f"BOT TRUCO OPTION {truco_available_options} && CARDS STATUS {cards_status}")
        if self.ENVIDO in truco_available_options.values():
            bot_action = self.ask_envido(envido_calls_history, bet_on_table)
        if bot_action != self.PASS: return bot_action
        #"else"
        return self._handle_truco_calls(cards_status, truco_calls_history, truco_available_options[0], hand)
         
     ######### END OF TRUCO FUNCTIONS #########   
        

    def play_card(self, other_player_movement: Movement, hand: int, envido_calls_history: dict[str, int], truco_calls_history: dict[str, int]) -> Movement:
        is_last_move_bet: bool = other_player_movement['is_bet']
        last_action: PlayerAction = other_player_movement['player_action']
        self.playing_envido = last_action in envido_calls_history and is_last_move_bet
        self.playing_truco = last_action in truco_calls_history and is_last_move_bet
        # bot_bet_response: Bet = ''
        # bot_action: PlayerAction = ''
        if self.playing_envido:
            bot_bet_response: Bet = self.ask_envido(envido_calls_history, last_action)
            return self._return_player_movement(True, bot_bet_response)
        
        elif self.playing_truco: 
            bot_bet_response: Bet = self.ask_truco(truco_calls_history, envido_calls_history, last_action, hand)
            return self._return_player_movement(True, bot_bet_response)
        
        else: 
            bot_bet_response: Bet = self.ask_truco(truco_calls_history, envido_calls_history, last_action, hand)
            print(bot_bet_response)
            if bot_bet_response != self.PASS:
                return self._return_player_movement(True, bot_bet_response)
            print("TIME TO PLAY CARD")
