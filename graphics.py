from tkinter import *
import math


class Graphics:
    """GUI for inputting sudoku puzzle to be solved."""
    def __init__(self, parent, size):
        self.values = [[0 for i in range(size)] for j in range(size)]
        self.entries = []
        self.create_grid(parent)
        self.button = Button(parent, text="Solve", command=self.button_press)
        self.button.grid(row=len(self.values), columnspan=len(self.values))

    def create_grid(self, parent):
        for i in range(len(self.values)):
            for j in range(len(self.values)):
                temp = Entry(parent)
                temp.grid(row=i, column=j)
                self.entries.append(temp)

    def button_press(self):
        for i in range(len(self.entries)):
            if self.entries[i].get() != '':
                I = math.floor(i / len(self.values))
                J = i % len(self.values)
                self.values[I][J] = int(self.entries[i].get())
