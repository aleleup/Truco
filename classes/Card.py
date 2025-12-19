from constants.emojis import *
class Card:
    # name: str
    # value: int
    # type: str
    # envido_value: int
    emoji_store: dict[str, str] 
    def __init__(self, number: int,  type: str, value: int, envido_value: int, ascii_art: str) -> None:
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
        self.ascii_art: str = ascii_art

    def to_dict(self) -> dict[str, str | int]:
        return {
            'name': self.name,
            'value': self.value,
            'type': self.type,
            'envido_value': self.envido_value,
            'ascii_art': self.ascii_art
        }