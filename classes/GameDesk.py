from constants.types import *
from constants.bets import *
from classes.TrucoDeck import *
from classes.Player import Player
from classes.PlayersActions import PlayersActions
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
        self.in_bet: bool = False
        # self._current_bet: list[str] = [] #0: bet type. 1: real bet
        self._bet_on_the_desk: dict[int, list[str]] = {}
        # Hand and round
        self._round: int = -1
        self.hand: int = 0


    ########PLAYERS MANAGEMENT########
    def _set_hand_and_foot_players(self) -> None:
        if self._round % 2 == 0:
            self._hand_player = self._player_0
            self._foot_player = self._player_1
        else:
            self._hand_player = self._player_1
            self._foot_player = self._player_0


    def players_status(self) -> list[PlayerStatus]:
        res = [self._hand_player.show_player_data(), self._foot_player.show_player_data()]
        return res 

    def init_row(self) -> list[PlayerStatus]:
        self._round += 1
        self.hand = 1
        new_row_cards: list[list[Card]] = self._deck.shuffle_cards()
        self._set_hand_and_foot_players()
        default_options: PlayerOptions = self._players_options_based_on_bet_calls()
        self._set_players_options(default_options)
        self._hand_player.set_cards(new_row_cards[0])
        self._foot_player.set_cards(new_row_cards[1])
        res = [self._hand_player.show_player_data(), self._foot_player.show_player_data()]
        return res

    def _players_options_based_on_bet_calls(self) -> PlayerOptions:
        '''deletes envido item from res if it completed it`s total calls'''
        res: PlayerOptions = {}
        envido_options: dict[int, str] = {}
        truco_option: str = TRUCO
        if self.hand == 1 and self._bet_calls.truco == 0: # if hand is 1 and there were no truco bet accepted:
            envido_options = {
                0: ENVIDO,
                1: REAL_ENVIDO,
                2: FALTA_ENVIDO,
            }
            if self._bet_calls.envido == 2:
                del envido_options[0]
            if self._bet_calls.real_envido:
                if 0 in envido_options: del envido_options[0]
                del envido_options[1]
            if self._bet_calls.falta_envido:
                if 0 in envido_options: del envido_options[0]
                if 1 in envido_options: del envido_options[1]
                del envido_options[2]

        if self._bet_calls.truco:
            truco_option = RE_TRUCO
        elif self._bet_calls.re_truco:
            truco_option = VALE_CUATRO
        elif self._bet_calls.vale_cuatro: truco_option = ''

        if self.in_bet: 
            res["final_answer"] = {
                0: ACCEPT,
                1: DONT_ACCEPT
            }
        res[TRUCO] = truco_option
        res[ENVIDO] = envido_options
        return res
    


    def show_player_data_by_id(self, id: int) -> PlayerStatus:
        if id == 0:
            return self._player_0.show_player_data()
        else:
            return self._player_1.show_player_data() 
        
    
    def _set_players_options(self, options: PlayerOptions):
        self._hand_player.set_options(options)
        self._foot_player.set_options(options)
    ##########################################


    ########### CARDS AND ACTIONS ############
    def _add_to_compare_list(self, id: int, index: int) -> dict[str,  int | bool]:
        if id == 0:
            self._cards_on_the_desk[0] = self._player_0.remove_card(index)
        else:
            self._cards_on_the_desk[1] = self._player_1.remove_card(index)
        if len(self._cards_on_the_desk) == 2: 
            comparasing_result: dict[str,  int | bool] = self._compare_cards()
            self._cards_on_the_desk.clear()
            return comparasing_result
        else: return {}
    

    def _compare_cards(self) -> dict[str, int | bool]:
        hand_winner: int
        if self._cards_on_the_desk[0].value == self._cards_on_the_desk[1].value:
            return {"tie": True}
        elif self._cards_on_the_desk[0].value > self._cards_on_the_desk[1].value:
            hand_winner = 0
        else: hand_winner = 1
        return  {"tie": False, 'winner': hand_winner} 
    


    def receive_players_action(self, id: int, player_action: PlayersActions) -> dict[str,  int | bool]:
        if len(player_action.bet) > 0:
            self._add_to_bet_list(id, player_action.bet)
        if player_action.card_index >= 0:
            return self._add_to_compare_list(id, player_action.card_index)
        return {}

    ################################################
    
    ###########         Points          ############

    def _add_points_to_envido_winner(self):
        # TODO: SEE cases of not accepting.
        envido_winner, envido_looser = self._compare_envidos_return_winner_and_looser()
        if self._bet_calls.latest[1] == FALTA_ENVIDO:
            envido_winner.add_points(30 - envido_looser.get_points() )
        points: int = self._bet_calls.return_envidos_total_points_in_bet()
        envido_winner.add_points(points)

    def _compare_envidos_return_winner_and_looser(self) -> list[Player]:
        hand_player_envido: int = self._hand_player.get_envido()
        foot_player_envido: int = self._hand_player.get_envido()
        if hand_player_envido == foot_player_envido: return [self._hand_player, self._foot_player]
        elif hand_player_envido > foot_player_envido: return [self._hand_player, self._foot_player] 
        else: return [self._foot_player, self._hand_player]
    
    def _add_to_bet_list(self, id: int, bet:list[str]):
        if bet[0] == FINAL_ANSWER and self._bet_calls.latest[0] == ENVIDO: 
            self.in_bet = False
            self._add_points_to_envido_winner()
        else:
            self.in_bet = True
            self._bet_on_the_desk[id] = bet
            self._bet_calls.upgrade_call(bet)
            self._set_players_options(self._players_options_based_on_bet_calls())

    # def _add_points_to_truco_winner(self):
    #     row_winner