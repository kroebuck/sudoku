# Sudoku Solver

from tkinter import *
from graphics import Graphics

side_length = 9

root = Tk()
root.title('Sudoku')
Graphics(root, side_length)
root.mainloop()
