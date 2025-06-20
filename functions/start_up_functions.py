def pop_lowest_val(l:list, prop:str) -> None:
    index: int = 0
    comp: int = 0
    for i in range(len(l)):
        if i == 0:
            comp = l[i][prop]
        if l[i][prop] < comp:
            index = i
            comp = l[i][prop]
    l.pop(index)

def calc_envido(cards: list[dict[str, str|int]]) -> int:
    '''First, I need to compare the fst card type with the second and the third, and if they have the same type then I'll 
    store it in a "Filtered" list. Now, If not all cards are in this filtered list (not all cards have the same type) I look 
    the second card and compare it to the third (last comparasion) and if they match I'll store it.
    If there's no match, I'll return the max envido_value of all of them.
    '''
    total_envido: int = 0
    same_type_list: list[dict[str, str| int]] = []
    i: int = 0
    while i < 3:
        # while it's not assure that i'll have more than one card of same type, return value updates to the max envido_value
        if cards[i]['envido_value'] > total_envido: total_envido = cards[i]['envido_value']
        j: int = i+1
        while j < len(cards):
            if cards[i]['type'] == cards[j]['type']:
                if cards[i] not in same_type_list: same_type_list.append(cards[i])
                if cards[j] not in same_type_list: same_type_list.append(cards[j])
            j+=1
        i+=1
    if not same_type_list: return total_envido
    if len(same_type_list) == len(cards):
        pop_lowest_val(same_type_list, 'envido_value')
    total_envido = 0
    for card in same_type_list:
        total_envido += card['envido_value']
    total_envido+= 20 
    return total_envido
