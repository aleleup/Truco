import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtCore import Qt
from functions.card_creation import create_deck
from functions.game_play import game_play
from test_functionalities.test_classes_functionalities import *

def render_truco() -> None:
    '''Orquestator and renderer of the game'''

    # root = tk.Tk()
    # root.geometry('700x500')

    # display_text = tk.Label(root=root, value=constants['title'])

    deck = create_deck()
    # print(deck)
    # game_play(deck)
    # test_bot_ask_truco(deck)
    test_first_interaction(deck)
render_truco()




def create_hello_window():
    """
    Creates and displays a simple PyQt6 window with a "Hello, PyQt!" message.
    """
    # 1. Create an instance of QApplication
    # Every PyQt application must create a QApplication object.
    # sys.argv allows command-line arguments to be passed to the application.
    app = QApplication(sys.argv)

    # 2. Create a basic QWidget (this will be our main window)
    window = QWidget()
    window.setWindowTitle("Te canto Truco") # Set the window title
    window.setGeometry(200, 200, 800, 800) # (x, y, width, height) of the window

    # 3. Create a QLabel (for displaying text)
    label = QLabel("Truco con PyQt!", parent=window) # Text and parent widget
    label.setFont(label.font()) # Get current font
    label_font = label.font()
    label_font.setPointSize(24) # Set font size
    label.setFont(label_font)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter) # Center the text

    # Position the label in the center of the window (basic positioning for now)
    # We'll learn about layout managers later for better positioning.
    label.setGeometry(300, 50, 200, 100) # Make label fill the window

    # 4. Show the window
    window.show()

    # 5. Start the application's event loop
    # This keeps the application running until the user closes the window.
    sys.exit(app.exec())

# if __name__ == "__main__":
#     create_hello_window()