from classes.bot import Bot
from classes.player import Player
from functions.deal_cards import handle_cards






def test_envido_bot(deck):
    envidos_calls: dict[str, int] = {
                'envido': 0,
                'real_envido': 0,
                'falta_envido': 0
            }
    cards = handle_cards(deck, [])
    game_instance = 2
    bot = Bot(cards, 0, 0, 30)
    bot.calc_envido()
    print(f"{cards[0]['card_ascii_art']}, {cards[1]['card_ascii_art']}, {cards[2]['card_ascii_art']}")
    print(bot.total_envido)
    print(bot.ask_envido(game_instance, envidos_calls, ''))


def test_player(deck):
    envidos_calls: dict[str, int] = {
                'envido': 2,
                'real_envido': 0,
                'falta_envido': 0
            }
    cards = handle_cards(deck, [])
    game_instance = 1
    player = Player(cards, 0, 0, 30)
    player.calc_envido()
    print(f"{cards[0]['card_ascii_art']}, {cards[1]['card_ascii_art']}, {cards[2]['card_ascii_art']}")
    print(player.total_envido)
    print(player.ask_envido(game_instance, envidos_calls, 'envido'))

