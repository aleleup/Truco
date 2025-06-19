import tkinter as tk
from functions.card_creation import create_deck
from functions.game_play import game_play

def render_truco() -> None:
    '''Orquestador e inicializador del programa'''

    root = tk.Tk()
    root.geometry('700x500')

    # display_text = tk.Label(root=root, value=constants['title'])

    deck = create_deck()
    game_play(deck)

    # root.mainloop()


render_truco()
