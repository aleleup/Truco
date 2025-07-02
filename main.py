import tkinter as tk
from functions.card_creation import create_deck
# from functions.game_play import game_play
from test_functionalities.test_bot import test_envido_bot

def render_truco() -> None:
    '''Orquestador e inicializador del programa'''

    root = tk.Tk()
    root.geometry('700x500')

    # display_text = tk.Label(root=root, value=constants['title'])

    deck = create_deck()
    # print(deck)
    # game_play(deck)
    test_envido_bot(deck)
    # root.mainloop()


render_truco()
