# Sudoku Solver

from tkinter import *
from graphics import Graphics
from grid import Grid

side_length = 9

root = Tk()
root.title('Sudoku')
Graphics(root, side_length)
root.mainloop()

# initData = [[8, 0, 0, 9, 3, 0, 0, 0, 2],
#             [0, 0, 9, 0, 0, 0, 0, 4, 0],
#             [7, 0, 2, 1, 0, 0, 9, 6, 0],
#             [2, 0, 0, 0, 0, 0, 0, 9, 0],
#             [0, 6, 0, 0, 0, 0, 0, 7, 0],
#             [0, 7, 0, 0, 0, 6, 0, 0, 5],
#             [0, 2, 7, 0, 0, 8, 4, 0, 6],
#             [0, 3, 0, 0, 0, 0, 5, 0, 0],
#             [5, 0, 0, 0, 6, 2, 0, 0, 8]]
