# import json, asyncio
# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from classes.GameDesk import GameDesk
# from classes.ConnectionManager import ConnectionManager
from constants.types import *
from constants.bets import *
import unittest
# from pydantic import BaseModel
class TestGameDesk(unittest.TestCase):
    def _see_options_and_turns_assertions(self, desk: GameDesk, options: PlayerOptions, player_id_turn: int):
        player0_status: PlayerStatus = desk.player_status(0)
        self.assertEqual(player0_status["options"], options)
        ### PLAYER 1 ###
        player1_status: PlayerStatus = desk.player_status(1)
        self.assertEqual(player1_status["options"], options)

        if player_id_turn == 0:
            self.assertTrue(player0_status["is_player_turn"])
            self.assertFalse(player1_status["is_player_turn"])
        if player_id_turn == 1:
            self.assertTrue(player1_status["is_player_turn"])
            self.assertFalse(player0_status["is_player_turn"])

    def test_players_envido_nightmare_check(self):
        fst_options = {
            ENVIDO: [ENVIDO, REAL_ENVIDO, FALTA_ENVIDO],
            TRUCO: TRUCO
        }
        snd_options = {
            ENVIDO: [ENVIDO, REAL_ENVIDO, FALTA_ENVIDO],
            FINAL_ANSWER: [ACCEPT, DONT_ACCEPT],
            TRUCO: TRUCO
        }
        thrd_options = {
            ENVIDO: [REAL_ENVIDO, FALTA_ENVIDO],
            FINAL_ANSWER: [ACCEPT, DONT_ACCEPT],
            TRUCO: TRUCO
        }
        fourth_options = {
            ENVIDO: [FALTA_ENVIDO],
            FINAL_ANSWER: [ACCEPT, DONT_ACCEPT],
            TRUCO: TRUCO
        }
        fiveth_options = {
            ENVIDO: [],
            FINAL_ANSWER: [ACCEPT, DONT_ACCEPT],
            TRUCO: TRUCO
        }
        sixth_options: dict[str, list[str] | str] = {
            ENVIDO: [],
            TRUCO: TRUCO
        }
        

        desk: GameDesk = GameDesk()
        desk.init_round()

        ### FST OPTIONS ###
        self._see_options_and_turns_assertions(desk, fst_options, 0)
        
        # PLAYER 0 SAYS ENVIDO
        new_action = PlayersActions(card_index=-1, bet=[ENVIDO, ENVIDO])  
        desk.receive_players_action(0, new_action)

        ### SND OPTIONS ###
        self._see_options_and_turns_assertions(desk, snd_options, 1)

        # PLAYER 1 SAYS ENVIDO
        new_action = PlayersActions(card_index=-1, bet=[ENVIDO, ENVIDO])  
        desk.receive_players_action(1, new_action)

        ### 3TH OPTIONS ###
        self._see_options_and_turns_assertions(desk, thrd_options, 0)


        # PLAYER 0 SAYS REAL ENVIDO
        new_action = PlayersActions(card_index=-1, bet=[ENVIDO, REAL_ENVIDO])  
        desk.receive_players_action(0, new_action)

        ### 4TH OPTIONS ###
        self._see_options_and_turns_assertions(desk, fourth_options, 1)

        # PLAYER 1 SAYS FALTA ENVIDO
        new_action = PlayersActions(card_index=-1, bet=[ENVIDO, FALTA_ENVIDO])  
        desk.receive_players_action(1, new_action)

        ### 5TH OPTIONS ###
        self._see_options_and_turns_assertions(desk, fiveth_options, 0)


        # PLAYER 1 SAYS ACCEPT
        new_action = PlayersActions(card_index=-1, bet=[FINAL_ANSWER, ACCEPT])  
        desk.receive_players_action(1, new_action)

        ### 6TH OPTIONS ###
        self._see_options_and_turns_assertions(desk, sixth_options, 1)

    def test_truco_shooting_check(self):
        fst_options = {
            ENVIDO: [ENVIDO, REAL_ENVIDO, FALTA_ENVIDO],
            TRUCO: TRUCO
        }
        snd_options = {
            ENVIDO: [ENVIDO, REAL_ENVIDO, FALTA_ENVIDO],
            FINAL_ANSWER: [ACCEPT, DONT_ACCEPT],
            TRUCO: RE_TRUCO
        }
        thrd_options = {
            ENVIDO: [ENVIDO, REAL_ENVIDO, FALTA_ENVIDO],
            FINAL_ANSWER: [ACCEPT, DONT_ACCEPT],
            TRUCO: VALE_CUATRO
        }
        fourth_options = {
            ENVIDO: [ENVIDO, REAL_ENVIDO, FALTA_ENVIDO],
            FINAL_ANSWER: [ACCEPT, DONT_ACCEPT],
            TRUCO: ''
        }
        fiveth_options: PlayerOptions = {
            ENVIDO: [],
            # FINAL_ANSWER: [],
            TRUCO: ''
        }

        desk: GameDesk = GameDesk()
        desk.init_round()

        ### FST OPTIONS ###
        self._see_options_and_turns_assertions(desk, fst_options, 0)
        
        # PLAYER 0 SAYS TRUCO
        new_action = PlayersActions(card_index=-1, bet=[TRUCO, TRUCO])  
        desk.receive_players_action(0, new_action)

        ### SND OPTIONS ###
        self._see_options_and_turns_assertions(desk, snd_options, 1)

        # PLAYER 1 SAYS RE_TRUCO
        new_action = PlayersActions(card_index=-1, bet=[TRUCO, RE_TRUCO])  
        desk.receive_players_action(1, new_action)

        ### 3TH OPTIONS ###
        self._see_options_and_turns_assertions(desk, thrd_options, 0)


        # PLAYER 0 SAYS VALE CUATRO
        new_action = PlayersActions(card_index=-1, bet=[TRUCO, VALE_CUATRO])  
        desk.receive_players_action(0, new_action)

        ### 4TH OPTIONS ###
        self._see_options_and_turns_assertions(desk, fourth_options, 1)

        # PLAYER 1 SAYS ACCEPT
        new_action = PlayersActions(card_index=-1, bet=[FINAL_ANSWER, ACCEPT])  
        desk.receive_players_action(1, new_action)

        self._see_options_and_turns_assertions(desk, fiveth_options, 0)


    def test_truco_nightmare_check(self):
        fst_options = {
            ENVIDO: [ENVIDO, REAL_ENVIDO, FALTA_ENVIDO],
            TRUCO: TRUCO
        }
        snd_options = {
            ENVIDO: [ENVIDO, REAL_ENVIDO, FALTA_ENVIDO],
            FINAL_ANSWER: [ACCEPT, DONT_ACCEPT],
            TRUCO: RE_TRUCO
        }
        thrd_options: PlayerOptions = {
            ENVIDO: [],
            # FINAL_ANSWER: [ACCEPT, DONT_ACCEPT],
            TRUCO: RE_TRUCO
        }
        fourth_options: PlayerOptions = {
            ENVIDO: [],
            FINAL_ANSWER: [ACCEPT, DONT_ACCEPT],
            TRUCO: VALE_CUATRO            
        }
        fiveth_options: PlayerOptions = {
            ENVIDO: [],
            # FINAL_ANSWER: [ACCEPT, DONT_ACCEPT],
            TRUCO: VALE_CUATRO
        }
        sixth_options: PlayerOptions = {
            ENVIDO: [],
            FINAL_ANSWER: [ACCEPT, DONT_ACCEPT],
            TRUCO: ''
        }
        seventh_options: PlayerOptions = {
            ENVIDO: [],
            # FINAL_ANSWER: [ACCEPT, DONT_ACCEPT],
            TRUCO: ''
        }

        desk: GameDesk = GameDesk()
        desk.init_round()

        ### FST OPTIONS ###
        self._see_options_and_turns_assertions(desk, fst_options, 0)
        
        # PLAYER 0 SAYS TRUCO
        new_action = PlayersActions(card_index=-1, bet=[TRUCO, TRUCO])  
        desk.receive_players_action(0, new_action)

        ### SND OPTIONS ###
        self._see_options_and_turns_assertions(desk, snd_options, 1)

        # PLAYER 1 SAYS ACCEPT
        new_action = PlayersActions(card_index=-1, bet=[FINAL_ANSWER, ACCEPT])  
        desk.receive_players_action(1, new_action)

        ### 3TH OPTIONS ###
        self._see_options_and_turns_assertions(desk, thrd_options, 0)

        # Players Throw Cards:
        desk.receive_players_action(0, PlayersActions(card_index=0,bet=[]))
        desk.receive_players_action(1, PlayersActions(card_index=0,bet=[]))
        desk.receive_players_action(0, PlayersActions(card_index=0,bet=[]))


        # PLAYER 1 SAYS RE_TRUCO    
        new_action = PlayersActions(card_index=-1, bet=[TRUCO, RE_TRUCO])  
        desk.receive_players_action(1, new_action)

        ### 4TH OPTIONS ###
        self._see_options_and_turns_assertions(desk, fourth_options, 0)

        # PLAYER 0 SAYS ACCEPT
        new_action = PlayersActions(card_index=-1, bet=[FINAL_ANSWER, ACCEPT])  
        desk.receive_players_action(0, new_action)

        ### 5TH OPTIONS ###
        self._see_options_and_turns_assertions(desk, fiveth_options, 1)


        # PLAYER 1 PLAYS CARDS
        desk.receive_players_action(0, PlayersActions(card_index=0,bet=[]))

        #PLAYER 0 SAYS VALE CUATRO

        new_action = PlayersActions(card_index=-1, bet=[TRUCO, VALE_CUATRO])  
        desk.receive_players_action(0, new_action)

        # 6th OPTIONS
        self._see_options_and_turns_assertions(desk, sixth_options, 1)

        # PLAYER 1 SAYS ACCEPT
        new_action = PlayersActions(card_index=-1, bet=[FINAL_ANSWER, ACCEPT])  
        desk.receive_players_action(0, new_action)

        ### 7TH OPTIONS ###
        self._see_options_and_turns_assertions(desk, seventh_options, 0)
    
    def test_envido_invalidates_truco(self):
        fst_options = {
            ENVIDO: [ENVIDO, REAL_ENVIDO, FALTA_ENVIDO],
            TRUCO: TRUCO
        }
        snd_options = {
            ENVIDO: [ENVIDO, REAL_ENVIDO, FALTA_ENVIDO],
            FINAL_ANSWER: [ACCEPT, DONT_ACCEPT],
            TRUCO: RE_TRUCO
        }
        thrd_options = {
            ENVIDO: [ENVIDO, REAL_ENVIDO, FALTA_ENVIDO],
            FINAL_ANSWER: [ACCEPT, DONT_ACCEPT],
            TRUCO: TRUCO
        }
        fourth_options: PlayerOptions = {
            ENVIDO: [],
            # FINAL_ANSWER: [ACCEPT, DONT_ACCEPT],
            TRUCO: TRUCO
        }
        desk: GameDesk = GameDesk()
        desk.init_round()
        ### FST OPTIONS ###
        self._see_options_and_turns_assertions(desk, fst_options, 0)
        
        # PLAYER 0 SAYS TRUCO
        new_action = PlayersActions(card_index=-1, bet=[TRUCO, TRUCO])  
        desk.receive_players_action(0, new_action)

        ### SND OPTIONS ###
        self._see_options_and_turns_assertions(desk, snd_options, 1)

        # PLAYER 1 SAYS ENVIDO
        new_action = PlayersActions(card_index=-1, bet=[ENVIDO, ENVIDO])  
        desk.receive_players_action(1, new_action)

        ### THRD OPTIONS ###
        self._see_options_and_turns_assertions(desk, thrd_options, 0)

        #PLAYER 0 SAYS ACCEPT
        new_action = PlayersActions(card_index=-1, bet=[FINAL_ANSWER, ACCEPT])  
        desk.receive_players_action(0, new_action)

        ### SND OPTIONS ###
        self._see_options_and_turns_assertions(desk, fourth_options, 1)