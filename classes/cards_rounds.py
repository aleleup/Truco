from constants.types import *
from constants.status import *
from classes.player import Player


class CardRound:
    def __init__(self, player_0: Player, player_1: Player, deck: Deck):
        self.player_0 = player_0
        self.player_1 = player_1
        self.deck = deck
        self.round_status = ON_GOING
        self.envido_winner: int|None = None
        self.envido_points: int = 0
        self.truco_winner: int|None = None
        self.truco_points: int = 1 #At least it sums one
        

