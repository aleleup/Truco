from constants.types import *
from constants.bets import *
from classes.TrucoDeck import *
from classes.Player import Player
from classes.BetCallsHistory import BetCallsHistory
class GameDesk:
    # player_0: Player
    # player_1: Player
    # deck: TrucoDeck

    def __init__(self) -> None:
        # Deck
        
        self._deck = TrucoDeck()
        self._deck.create_deck()
        self._cards_on_the_desk :  dict[int, Card] = {} # should optimize list with arrays if they could store objects

        # Players:
        self._player_0 = Player(0)
        self._player_1 = Player(1)
        self._hand_player: Player
        self._foot_player: Player

        # Bet status management:
        self._bet_calls: BetCallsHistory = BetCallsHistory()
        self._in_bet: bool = False
        self._last_bet_accepted: bool = False
        
        # self._current_bet: list[str] = [] #0: bet type. 1: real bet
        self._bet_on_the_desk: dict[int, list[str]] = {}
        # Hand and round
        self._round: int = -1
        self._hand: int = 0
        # self._turn_counter: int = 0


    ######## DESK STATUS ########
    def get_round(self)-> int: return self._round
    def get_hand(self)-> int: return self._hand
    def game_over(self) -> bool: return False
    ######## PLAYERS MANAGEMENT ########
    def _set_hand_and_foot_players(self) -> None:
        if self._round % 2 == 0:
            self._hand_player = self._player_0
            self._foot_player = self._player_1
        else:
            self._hand_player = self._player_1
            self._foot_player = self._player_0
        self._hand_player.toggle_turn()



    def players_status(self) -> list[PlayerStatus]:
        res = [self._hand_player.status(), self._foot_player.status()]
        return res 

    def init_row(self):
        self._round += 1
        self._hand = 1
        new_row_cards: list[list[Card]] = self._deck.shuffle_cards()
        self._set_hand_and_foot_players()
        self._set_players_options()
        self._hand_player.set_cards(new_row_cards[0])
        self._foot_player.set_cards(new_row_cards[1])

    def _players_options_based_on_bet_calls(self) -> PlayerOptions:
        '''deletes envido item from res if it completed it`s total calls'''
        res: PlayerOptions = {}
        envido_options: list[str] = []
        truco_option: str = TRUCO
        if self._hand == 1 and not self._last_bet_accepted : # if hand is 1 and there were no truco bet accepted:
            envido_options = [ENVIDO, REAL_ENVIDO, FALTA_ENVIDO]
            if self._bet_calls.envido == 2:
                envido_options.pop(0)
            if self._bet_calls.real_envido:
                if ENVIDO in envido_options: envido_options.pop(0) # -> [R_E, F_E] 
                envido_options.pop(0) # -> [F_E] 
            if self._bet_calls.falta_envido:
                if ENVIDO in envido_options: envido_options.pop(0)
                if REAL_ENVIDO in envido_options: envido_options.pop(0)
                envido_options.pop(0)

        if self._bet_calls.truco:
            truco_option = RE_TRUCO
        if self._bet_calls.re_truco:
            truco_option = VALE_CUATRO
        if self._bet_calls.vale_cuatro: truco_option = ''

        if self._in_bet: 
            res[FINAL_ANSWER] = [ACCEPT, DONT_ACCEPT]

        res[TRUCO] = truco_option
        res[ENVIDO] = envido_options
        return res
    


    def player_status(self, id: int) -> PlayerStatus:
        if id == 0:
            return self._player_0.status()
        else:
            return self._player_1.status() 
        
    
    def _set_players_options(self):
        options: PlayerOptions = self._players_options_based_on_bet_calls()
        self._hand_player.set_options(options)
        self._foot_player.set_options(options)

    def _toggle_players_turn(self) -> None:
        self._hand_player.toggle_turn()
        self._foot_player.toggle_turn()

    ##########################################

    ########### CARDS AND ACTIONS ############
    def _add_to_compare_list(self, id: int, index: int):
        if id == 0:
            self._cards_on_the_desk[0] = self._player_0.remove_card(index)
        else:
            self._cards_on_the_desk[1] = self._player_1.remove_card(index)
        if len(self._cards_on_the_desk) == 2: 
            self._cards_on_the_desk.clear()
            self._hand += 1
    

    def _compare_cards(self) -> dict[str, int | bool]:
        hand_winner: int
        if self._cards_on_the_desk[0].value == self._cards_on_the_desk[1].value:
            return {"tie": True}
        elif self._cards_on_the_desk[0].value > self._cards_on_the_desk[1].value:
            hand_winner = 0
        else: hand_winner = 1
        return  {"tie": False, 'winner': hand_winner} 
    


    def receive_players_action(self, id: int, player_action: PlayersActions) -> None:
        if len(player_action.bet) > 0:
            self._add_to_bet_list(id, player_action.bet)
        if player_action.card_index >= 0:
            self._add_to_compare_list(id, player_action.card_index)
        self._toggle_players_turn()
        self._set_players_options()

    ################################################
    
    ###########         Points          ############

    def _add_points_to_envido_winner(self):
        envido_winner, envido_looser = self._compare_envidos_return_winner_and_looser()
        if self._bet_calls.latest[1] == FALTA_ENVIDO:
            envido_winner.add_points(30 - envido_looser.get_points() )
        points: int = self._bet_calls.return_envidos_total_points_in_bet()
        envido_winner.add_points(points)

    def _compare_envidos_return_winner_and_looser(self) -> list[Player]:
        hand_player_envido: int = self._hand_player.get_envido()
        foot_player_envido: int = self._foot_player.get_envido()
        print(hand_player_envido, foot_player_envido)
        if hand_player_envido == foot_player_envido: return [self._hand_player, self._foot_player]
        elif hand_player_envido > foot_player_envido: return [self._hand_player, self._foot_player] 
        else: return [self._foot_player, self._hand_player]
    
    def _add_to_bet_list(self, id: int, bet: list[str]):
        print(bet)
        if bet[0] == FINAL_ANSWER:
            print("TURNING BET OFF") 
            self._in_bet = False
            self._last_bet_accepted = True # Need this so none envido options is shown
            if self._bet_calls.latest[0] == ENVIDO:
                self._add_points_to_envido_winner()
            # if self._bet_calls.latest[0] == TRUCO: Point will be added when the row finishes
        else:
            self._in_bet = True
            self._bet_on_the_desk[id] = bet
            self._bet_calls.upgrade_call(bet)
        self._set_players_options()

    # def _add_points_to_truco_winner(self):
    #     row_winner