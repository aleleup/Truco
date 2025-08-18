from constants.types import *
from constants.status import *
from classes.player import Player
from random import randint
from database import SessionLocal
from databases.tables_schemas import CardRoundsTable
from constants.status import *
from fastapi import APIRouter

router = APIRouter()
db = SessionLocal()

class CardRound:
    def __init__(self, player_0: Player, player_1: Player, deck: Deck, game_num):
        self.player_0 = player_0
        self.player_1 = player_1
        self.deck = deck
        self.round_status = ON_GOING
        self.envido_winner: int|None = None
        self.envido_points: int = 0
        self.truco_winner: int|None = None
        self.truco_points: int = 1 #At least it sums one
        self.game_num: int = game_num
        
    def _deal_cards(self, cards_in_use: Deck) -> Deck:
        '''Searches in deck randomly a card and when 3 were selected = returns the hand'''
        i: int = 1
        res: Deck = []
        while i <=3 :
            card_index: int = randint(0, 39)
            card: Card = self.deck[card_index]

            if card not in cards_in_use:
                res.append(card)
                cards_in_use.append(card)
                i+=1
            
        return res    

    def _deal_cards_based_on_who_is_hand(self) -> None:
        '''Depending on who's receiving the cards first, you might have more chances on having a better play'''
        cards_in_use: Deck = []
        if self.player_0.is_player_the_hand(self.game_num):
            self.player_0.cards = self._deal_cards(cards_in_use)
            self.player_1.cards = self._deal_cards(cards_in_use)
        else:
            self.player_1.cards = self._deal_cards(cards_in_use)   
            self.player_0.cards = self._deal_cards(cards_in_use)
   
    def start_round(self):
        ''''''
        self._deal_cards_based_on_who_is_hand()
        ###Viewing cards
        self.player_0.print_cards()
        self.player_1.print_cards()

        # card_round = CardRoundsTable(
        #     status = self.round_status,
        #     envido_winner = self.envido_winner,
        #     envido_points = self.envido_points,
        #     truco_winner = self.truco_winner,
        #     truco_points = self.truco_points,
        #     player_0_cards = self.player_0.cards,
        #     player_1_cards = self.player_1.cards,
        #     )

        # db.add(card_round)
        # db.commit()
        # db.refresh(card_round)


        #self route_
    # @router.
    # def 