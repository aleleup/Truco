from constants.types import *
from constants.status import *
from classes.player import Player
class GameTableClass:
    def __init__(self, deck: Deck):
        self.deck = deck
        self.player_0 = Player(0)
        self.player_1 = Player(1)
        self.winner_id: int|None = None
        self.game_status: str = ON_GOING #or FINISHED
