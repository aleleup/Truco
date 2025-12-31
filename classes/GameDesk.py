from constants.types import *
from constants.bets import *
from classes.TrucoDeck import *
from classes.Player import Player
from classes.BetCallsHistory import BetCallsHistory
class GameDesk:
    def __init__(self) -> None:
        # Deck
        
        self._deck = TrucoDeck()
        self._deck.create_deck()
        self._cards_on_the_desk :  dict[int, list[Card]] = {0: [], 1: []} # should optimize list with arrays if they could store objects

        # Players:
        self._player_0 = Player(0)
        self._player_1 = Player(1)
        self._hand_player: Player
        self._foot_player: Player
        self._player_id_turn_saver: int
        self._winner_id: int = -1
        # Bet status management:
        self._bet_calls: BetCallsHistory
        
        # self._bet_on_the_desk: dict[int, list[str]] = {}
        # Hand and round
        self._round: int = -1
        # self._turn_counter: int = 0
        self._round_winner_id: int = -1


    #################### PUBLIC METHODS ####################

    def init_round(self):
        self._check_winner()
        self._round += 1
        self._round_winner_id = -1
        self._player_id_turn_saver: int = -1

        self._bet_calls = BetCallsHistory()
        self._clear_public_data()
        new_row_cards: list[list[Card]] = self._deck.shuffle_cards()
        self._set_hand_and_foot_players()
        self._hand_player.set_cards(new_row_cards[0])
        self._foot_player.set_cards(new_row_cards[1])
        self._hand_player.set_quiero(True)
        self._foot_player.set_quiero(True)

        self._hand_player.set_turn(True)
        self._foot_player.set_turn(False)
        self._set_players_options()

    def player_status(self, id: int) -> PlayerStatus:
        if id == 0:
            return self._player_0.status(self._bet_calls.in_bet)
        else:
            return self._player_1.status(self._bet_calls.in_bet) 
        
        
    def receive_players_action(self, id: int, player_action: PlayersActions) -> None:
        if len(player_action.bet) > 0:
            self._add_to_bet_list(id, player_action.bet)
        elif player_action.card_index >= 0:
            self._add_to_compare_list(id, player_action.card_index)
            if len(self._cards_on_the_desk[0]) == len(self._cards_on_the_desk[1]):
                print("CHECKING ROUND WINNER IF THERE IS ONE")
                winner_id: int = self._compare_cards_and_return_winner() # returns -1 if none winner yet. else 0 or 1
                self._set_turn_to_round_winner()
                self._set_players_options()
                if winner_id in [0,1]:
                    self._add_points_to_truco_winner(winner_id)
                    self._check_winner()
                    self._round_winner_id = winner_id
                return                       
        self._toggle_players_turn()
        self._set_players_options()

    def get_general_view(self) -> dict[str, list[PlayerPublicData] | bool | int]:
        players_public_data: list[PlayerPublicData] = []
        for i in [0, 1]:
            public_data: PlayerPublicData = {
                'cards_on_desk': self._show_cards(self._cards_on_the_desk[i]),
                'last_bet': self._bet_calls.latest_by_id[i],
                'points': self._get_player_by_id(i).get_points()
            }
            players_public_data.append(public_data)
        
        return {
            'players_public_data': players_public_data, 
            'round': self._round,
            'round_winner': self._round_winner_id,
            'winner_id': self._winner_id
            }

    ########################################################


    ########### PRIVATE METHODS ###########

    ######## DESK STATUS ########


    def _in_first_hand(self) -> bool:
        return len(self._cards_on_the_desk[0]) == 0 or len(self._cards_on_the_desk[1]) == 0
    
    ######## PLAYERS MANAGEMENT ########
    def _set_hand_and_foot_players(self) -> None:
        if self._round % 2 == 0:
            self._hand_player = self._player_0
            self._foot_player = self._player_1
        else:
            self._hand_player = self._player_1
            self._foot_player = self._player_0

   
    def _players_options_based_on_bet_calls(self) -> PlayerOptions:
        res: PlayerOptions = {}
        envido_options: list[str] = []
        truco_option: list[str] = [TRUCO]
        print("DEBUG IN FIRST HAND", self._in_first_hand(), self._cards_on_the_desk)

        if self._in_first_hand() and not self._bet_calls.last_bet_accepted : # if hand is 1 and there were no truco bet accepted:
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
            truco_option = [RE_TRUCO]
        if self._bet_calls.re_truco:
            truco_option = [VALE_CUATRO]
        if self._bet_calls.vale_cuatro or self._bet_calls.in_bet and self._bet_calls.latest[0] == ENVIDO: truco_option = []

        if self._bet_calls.in_bet: 
            if self._bet_calls.latest[0] == TRUCO: truco_option += [ACCEPT, DONT_ACCEPT]
            if self._bet_calls.latest[0] == ENVIDO: envido_options += [ACCEPT, DONT_ACCEPT]
        
        print("ENVIDO_OPTIONS", envido_options)
        res[TRUCO] = truco_option
        res[ENVIDO] = envido_options
        res[ABANDON] = [ABANDON]
        return res
    

    
    def _set_players_options(self):
        options: PlayerOptions = self._players_options_based_on_bet_calls()
        self._hand_player.set_options(options)
        self._foot_player.set_options(options)

    def _toggle_players_turn(self) -> None:
        if not self._bet_calls.in_bet and self._player_id_turn_saver != -1:
            self._get_player_by_id(self._player_id_turn_saver).set_turn(True)
            self._get_player_by_id((self._player_id_turn_saver + 1) % 2).set_turn(False)
            self._player_id_turn_saver = -1
        else:
            self._hand_player.toggle_turn()
            self._foot_player.toggle_turn()

    def _set_turn_to_round_winner(self) -> None:
        last_card_0: Card = self._cards_on_the_desk[0][-1]
        last_card_1: Card = self._cards_on_the_desk[1][-1]

        if last_card_0.value == last_card_1.value: self._toggle_players_turn()
        elif last_card_0.value > last_card_1.value:
            self._player_0.set_turn(True)
            self._player_1.set_turn(False)

        else:
            self._player_1.set_turn(True)
            self._player_0.set_turn(False)


    ##########################################

    ########### CARDS AND ACTIONS ############
    def _add_to_compare_list(self, id: int, index: int):
        if id == 0:
            self._cards_on_the_desk[0].append(self._player_0.remove_card(index))
        else:
            self._cards_on_the_desk[1].append(self._player_1.remove_card(index))

    

    def _compare_cards_and_return_winner(self) -> int: #id
        hands_by_0: int = 0
        hands_by_1: int = 0
        fst_hand_winner: int = -1
        tie_on_fst_hand: bool = False
        # tie_on_other_hand: bool = False
        if self._in_first_hand(): return -1

        for card_index in range(0, len(self._cards_on_the_desk[0])):
            if card_index == 0:
                if self._has_greater_card_value_at_index(0, 1, card_index):
                    hands_by_0 += 1
                    fst_hand_winner = 0 
                elif self._has_greater_card_value_at_index(1, 0, card_index): 
                    hands_by_1 += 1
                    fst_hand_winner = 1
                else:
                    tie_on_fst_hand = True
            else:
                if tie_on_fst_hand:
                    if self._has_greater_card_value_at_index(0, 1, card_index): return 0
                    elif  self._has_greater_card_value_at_index(1, 0, card_index): return 1
                    #  I don't care if there's tie once again
                # else:
                if self._has_greater_card_value_at_index(0, 1, card_index): 
                    hands_by_0 += 1
                if self._has_greater_card_value_at_index(1, 0, card_index): 
                    hands_by_1 += 1
                else: # TIE:
                    if fst_hand_winner == 0: return 0
                    if fst_hand_winner == 1: return 1

        if hands_by_0 > 1 and hands_by_0 > hands_by_1: return 0
        if hands_by_1 > 1 and hands_by_1 > hands_by_0: return 1
        if len(self._cards_on_the_desk[0]) == 3 and hands_by_0 == 0 and hands_by_1 == 0: return self._hand_player.get_id()
        # None winner yet
        return -1

    def _has_greater_card_value_at_index(self, x:int, y:int, card_index: int) -> bool: 
        '''PC RESTARTING NOW!!!'''
        return self._cards_on_the_desk[x][card_index].value > self._cards_on_the_desk[y][card_index].value

    ################################################
    
    ###########         Points          ############

    def _add_points_to_envido_winner(self):
        envido_winner, envido_looser = self._compare_envidos_return_winner_and_looser()
        if self._bet_calls.latest[1] == FALTA_ENVIDO:
            envido_winner.add_points(30 - envido_looser.get_points() )
        points: int = self._bet_calls.return_envidos_total_points_in_bet()
        envido_winner.add_points(points)

    def _add_points_to_truco_winner(self, id: int):
        winner_player: Player = self._get_player_by_id(id)
        winner_player.add_points(self._bet_calls.return_truco_total_points_in_bet())


    def _compare_envidos_return_winner_and_looser(self) -> list[Player]:
        hand_player_envido: int = self._hand_player.get_envido()
        foot_player_envido: int = self._foot_player.get_envido()
        # if hand_player_envido == foot_player_envido: return [self._hand_player, self._foot_player]
        if hand_player_envido >= foot_player_envido: return [self._hand_player, self._foot_player] 
        else: return [self._foot_player, self._hand_player]
    
    def _add_to_bet_list(self, id: int, bet: list[str]) -> None:
        if bet[1] == ABANDON or (bet == [TRUCO, DONT_ACCEPT]) :
            winner_id: int = (id + 1) % 2
            winner_player: Player = self._get_player_by_id(winner_id)
            if self._in_first_hand():
                envido_points: int = self._bet_calls.return_envidos_total_points_in_bet()
                winner_player.add_points(envido_points)
            self._add_points_to_truco_winner(winner_id)
            self._check_winner()
            self._round_winner_id = winner_id
            # self.init_round()

        if bet[1] in FINAL_ANSWER:
            self._bet_calls.in_bet = False
            self._bet_calls.last_bet_accepted = True # Need this so none envido options is shown
            if bet[0] == ENVIDO:
                self._add_points_to_envido_winner()
                self._check_winner()
        
        else:
            if self._player_id_turn_saver == -1: self._player_id_turn_saver = id
            self._bet_calls.in_bet = True
            if bet[0] == TRUCO:
                if not self._bet_calls.truco: 
                    self._get_player_by_id(id).set_quiero(False)
                    # Other player should keep TRUE as default at init_round
                else: 
                    self._player_0.toggle_quiero()
                    self._player_1.toggle_quiero()

        self._bet_calls.upgrade_call(bet)
        self._bet_calls.latest_by_id[id] = bet[1]

    def _get_player_by_id(self, id: int) -> Player:
        if id == 0: return self._player_0
        else: return self._player_1

        

    ########## Code replicated!!!! ####### HOT FIX
    def _show_cards(self, cards: list[Card]) -> list[dict[str, str | int]]: 
        res: list[dict[str, str | int]] = []
        for card in cards:
            res.append(card.to_dict())
        return res
    

    def _clear_public_data(self) -> None:
        for i in self._cards_on_the_desk:
            self._cards_on_the_desk[i].clear()
            self._bet_calls.latest_by_id[i] = ''


    def _check_winner(self) -> None:
        for i in [0,1]:
            if self._get_player_by_id(i).get_points() == 30: self._winner_id = i