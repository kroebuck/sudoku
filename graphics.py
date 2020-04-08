from tkinter import *
import math
from grid import Grid


class Graphics:
    """GUI for inputting sudoku puzzle to be solved."""
    def __init__(self, parent, size):
        self.values = [[0 for i in range(size)] for j in range(size)]
        self.entries = []
        self.create_grid(parent)
        self.button = Button(parent, text="Solve", command=self.button_press)
        self.button.grid(row=len(self.values), columnspan=len(self.values))
        self.size = size

    def create_grid(self, parent):
        for i in range(len(self.values)):
            for j in range(len(self.values)):
                temp = Entry(parent)
                temp.grid(row=i, column=j)
                temp.config(width=2, justify=CENTER, font="Helvetica 35 bold")
                self.entries.append(temp)

    def button_press(self):
        for i in range(len(self.entries)):
            if self.entries[i].get() != '':
                k = math.floor(i / len(self.values))
                l = i % len(self.values)
                self.values[k][l] = int(self.entries[i].get())
        self.run_grid()

    def run_grid(self):
        puzzle = Grid(self.values, int(self.size / 3))

        if puzzle.grid_validate():
            sweep_count = 0
            while puzzle.grid_sweep():
                sweep_count += 1

            puzzle.output_solution()
            puzzle.grid_validate()

        for i in range(puzzle.box_size * puzzle.box_size):
            for j in range(puzzle.box_size * puzzle.box_size):
                index = i * puzzle.box_size * puzzle.box_size + j
                self.entries[index].delete(0, END)
                self.entries[index].insert(0, puzzle.grid[i][j].known)

