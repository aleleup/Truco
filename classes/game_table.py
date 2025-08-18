from constants.types import *
from constants.status import *
from classes.player import Player
from classes.cards_rounds import CardRound
from functions.card_creation import create_deck
class GameTableClass:
    def __init__(self):
        self.deck = create_deck()
        self.player_0 = Player(0)
        self.player_1 = Player(1)
        self.winner_id: int|None = None
        self.game_status: str = ON_GOING #or FINISHED
    
    def game_over(self) -> bool:
        return self.player_0.points >= 30 or self.player_1.points >= 30
             
    def start_game(self):
        ''''''
        card_round: object = CardRound(deck=self.deck, player_0=self.player_0, player_1=self.player_1, game_num=0)
        card_round.start_round()

