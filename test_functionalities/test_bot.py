from classes.bot import Bot
from functions.deal_cards import handle_cards


envidos_calls: dict[str, int] = {
                'envido': 0,
                'real_envido': 0,
                'falta_envido': 0
            }



def test_envido_bot(deck):
   
    cards = handle_cards(deck, [])
    game_instance = 2
    bot = Bot(cards, 0, 0, 30)
    bot.calc_envido()
    print(f"{cards[0]['card_ascii_art']}, {cards[1]['card_ascii_art']}, {cards[2]['card_ascii_art']}")
    print(bot.total_envido)
    print(bot.asks_envido(game_instance, envidos_calls, ''))

