"""interface.py

contains the GUI
"""

from pathlib import Path
from tkinter import messagebox, ttk

import pygubu


class Board():
    """Main class for the board"""

    def __init__(self, master):
        # pylint: disable= W0640
        self.master = master
        self.builder = pygubu.Builder()
        # styles
        style = ttk.Style()
        style.configure(
            "red.game.TButton", foreground="red", background='red')
        style.configure(
            "blue.game.TButton", foreground="blue", background='blue')
        # load the files
        self.builder.add_from_file(Path(__file__) / 'guis' / 'board.ui')
        self.main = self.builder.get_object('main', master)
        self.master.protocol("WM_DELETE_WINDOW", self.quit)
        self.builder.connect_callbacks(self)
        self.builder.import_variables(self)
        # attributes
        self.players = [None, None]
        self.state = None
        # configure interface
        self.grid = []
        for i in range(3):
            row = []
            for j in range(3):
                button = self.builder.get_object('B%s' % (3 * i + j + 1))
                func = lambda event, arg=(i, j): self.grid_clicked(event, arg)
                button.bind("<ButtonPress-1>", func)
                row.append(button)
            self.grid.append(row)
        self.b_p1 = self.builder.get_object('B_P1')
        self.b_p2 = self.builder.get_object('B_P2')

    # Callbacks

    def p1_pressed(self):
        """callback for B_P1"""
        if self.players[0] is None:
            self.players[0] = False
        else:
            self.players[0] = not self.players[0]
        self.b_p1['text'] = 'X: IA' if self.players[0] else 'X: Human'

    def p2_pressed(self):
        """callback for B_P2"""
        if self.players[1] is None:
            self.players[1] = False
        else:
            self.players[1] = not self.players[1]
        self.b_p2['text'] = 'O: IA' if self.players[1] else 'O: Human'

    def start_pressed(self):
        """callback for start button"""
        print('start pressed')

    def grid_clicked(self, event, arg):
        """handles the user input"""
        del event
        print(arg, 'clicked')

    # Control

    def quit(self):
        """Closes the Interface"""
        answer = messagebox.askyesno(
            message='Are you sure you want to close the game?',
            icon='question',
            title='Exit?',
            parent=self.master,
            default='no')
        if answer:
            self.master.destroy()
