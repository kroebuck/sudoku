# Sudoku Solver

from grid import Grid
from gridelement import GridElement

# use tkinter for UI?
initData = [[8, 0, 0, 9, 3, 0, 0, 0, 2],
            [0, 0, 9, 0, 0, 0, 0, 4, 0],
            [7, 0, 2, 1, 0, 0, 9, 6, 0],
            [2, 0, 0, 0, 0, 0, 0, 9, 0],
            [0, 6, 0, 0, 0, 0, 0, 7, 0],
            [0, 7, 0, 0, 0, 6, 0, 0, 5],
            [0, 2, 7, 0, 0, 8, 4, 0, 6],
            [0, 3, 0, 0, 0, 0, 5, 0, 0],
            [5, 0, 0, 0, 6, 2, 0, 0, 8]]

archie = Grid(initData)

known = 0
for i in range(9):
    for j in range(9):
        if hasattr(archie.grid[i][j], 'known'):
            #known += 1
            print("1")

print('known:', known)
print('unknown:', 81-known)

print(archie.grid[4][3].known)