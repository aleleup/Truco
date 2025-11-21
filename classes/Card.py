from constants.emojis import *
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
        self.envido_value: int = envido_value
        
        