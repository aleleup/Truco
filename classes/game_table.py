from constants.types import *
from constants.status import *
from classes.player import Player
from classes.cards_rounds import CardRound
class GameTableClass:
    def __init__(self, deck: Deck):
        self.deck = deck
        self.player_0 = Player(0)
        self.player_1 = Player(1)
        self.winner_id: int|None = None
        self.game_status: str = ON_GOING #or FINISHED


    def start_game(self):
        ''''''
        card_round: object = CardRound(deck=self.deck, player_0=self.player_0, player_1=self.player_1)
        card_round.game_num = 0
        card_round.start_round()