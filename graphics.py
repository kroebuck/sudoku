from tkinter import *
import math
from sudoku import Sudoku


class Graphics:
    """GUI for inputting sudoku puzzle to be solved."""
    def __init__(self, parent, size):
        self.size = size
        self.values = [[0 for i in range(size)] for j in range(size)]
        self.entries = []
        self.create_grid(parent)
        self.button_solve = Button(parent, text='Solve', command=self.button_solve_press)
        self.button_solve.grid(row=len(self.values), columnspan=len(self.values))

    def create_grid(self, parent):
        box_size = int(self.size/3)
        for i in range(len(self.values)):
            for j in range(len(self.values)):
                temp = Entry(parent)
                temp.grid(row=i, column=j)
                box_number = box_size * math.floor(i/box_size) + math.floor(j/box_size)
                if box_number % 2:
                    temp.config(width=2, justify=CENTER, font='Helvetica 35 bold', bg='#d9d9d9')
                else:
                    temp.config(width=2, justify=CENTER, font='Helvetica 35 bold')
                self.entries.append(temp)

    def button_solve_press(self):
        for i in range(len(self.entries)):
            if self.entries[i].get() != '':
                k = math.floor(i / len(self.values))
                l = i % len(self.values)
                self.values[k][l] = int(self.entries[i].get())
        self.run_grid()

    def run_grid(self):
        puzzle = Sudoku(self.values, int(self.size / 3))

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
                if not puzzle.grid[i][j].original:
                    self.entries[index].config(fg='#534aff')
