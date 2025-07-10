from classes.player_basics import PlayerBasics
def handle_envido_points(hand_player:PlayerBasics,  other_player:PlayerBasics, envido_calls_history: dict[str, int], bets_on_table:dict[int, str]):
    bets_values: list[str] = bets_on_table.values()
    if 'accept' in bets_values:
        if hand_player.total_envido >= other_player.total_envido: 
            hand_player.add_envido_points(envido_calls_history)
        else:
            other_player.add_envido_points(envido_calls_history)
    if 'dont_accept' in bets_values:
        if bets_on_table[hand_player.player_num] == 'dont_accept':
            other_player.add_unwanted_envido_points(envido_calls_history)
        else:
            hand_player.add_unwanted_envido_points(envido_calls_history)

    

def play_envido(hand_player:PlayerBasics, other_player:PlayerBasics) -> None:
    '''hand_player starts the envido bets and the bet rices depending on other_players decisions'''
    envidos_calls: dict[str, int] = {
                'envido': 0,
                'real_envido': 0,
                'falta_envido': 0
            }
    hand_player_num: int = hand_player.player_num
    other_player_num: int = other_player.player_num

    bets_on_table: dict[int, str] = {
        hand_player_num: '',
        other_player_num: ''
    }
    while bets_on_table[other_player_num] not in ['accept', 'dont_accept', 'pass'] :
            
            bets_on_table[hand_player_num] = hand_player.ask_envido(envidos_calls, bets_on_table[other_player_num])
            print(f"hand player says {bets_on_table[hand_player_num]}")

            if bets_on_table[hand_player_num] in ['accept', 'dont_accept']: break 

            bets_on_table[other_player_num] = other_player.ask_envido(envidos_calls, bets_on_table[hand_player_num])
            print(f"other player says {bets_on_table[other_player_num]}")
    print('###############################################################')

    handle_envido_points(hand_player, other_player, envidos_calls, bets_on_table)

