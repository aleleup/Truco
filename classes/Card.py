from constants.emojis import *
from constants.types import CardDict
class Card:
    # name: str
    # value: int
    # type: str
    # envido_value: int
    emoji_store: dict[str, str] 
    def __init__(self, number: int,  type: str, value: int, envido_value: int) -> None:
        self.emoji_store: dict[str, str] = {
            'sword': SWORD_EMOJI,
            'wood': WOOD_EMOJI,
            'gold': GOLD_EMOJI,
            'cup': CUP_EMOJI,
        }
        self.name: str = f'{number} {self.emoji_store[type]}'
        self.value: int = value
        self.type: str = type
        self.number: int = number
        self.envido_value: int = envido_value

    def to_dict(self) -> CardDict:
        return {
            'name': self.name,
            'value': self.value,
            'type': self.type,
            'number': self.number,
            'envido_value': self.envido_value,
        }