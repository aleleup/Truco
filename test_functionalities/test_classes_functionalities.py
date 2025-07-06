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
                'envido': 1,
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



def test_player_to_bot_envido(deck):
    

    player = Player([],0, 0, 30 )
    bot = Bot([],0, 0, 30 )
    
    game_instance = 1
    i:int = 0
    while i <= 10:
        cards_in_use = []
        player.cards = handle_cards(deck, cards_in_use )
        bot.cards = handle_cards(deck, cards_in_use )

        player.calc_envido()
        bot.calc_envido()
        envidos_calls: dict[str, int] = {
                'envido': 0,
                'real_envido': 0,
                'falta_envido': 0
            }
        bet_on_table:str = ''
        print('################')
        while bet_on_table not in ['accept', 'dont_accept']:
            bet_on_table = bot.ask_envido(game_instance, envidos_calls, bet_on_table)

            print(f"bot says {bet_on_table}")
            if bet_on_table in ['accept', 'dont_accept']: break 

            print("player envido", player.total_envido)
            bet_on_table = player.ask_envido(game_instance, envidos_calls, bet_on_table)
        print('###############################################################')
        print(f'player_envido: {player.total_envido}. bot_envido: {bot.total_envido}')
        
        i+=1    