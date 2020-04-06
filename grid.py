import math
from gridelement import GridElement


class Grid:
    def __init__(self, init_data):
        self.length = len(init_data)
        self.grid = [[GridElement(init_data[j][i]) for i in range(self.length)] for j in range(self.length)]

        for i in range(self.length):
            result_row = self.row_validate(i)
            result_column = self.column_validate(i)
            result_box = self.box_validate(i)
            if not result_row or not result_column or not result_box:
                print('Invalid initial grid!')
                return

        sweep_result = self.grid_sweep()
        while sweep_result:
            sweep_result = self.grid_sweep()

    def row_validate(self, row_number):
        """Checks if there are any duplicates in a given row, and updates empty square options."""
        values = [0 for i in range(self.length)]

        for i in range(self.length):
            if hasattr(self.grid[row_number][i], 'known'):
                if values[self.grid[row_number][i].known - 1] == 0:
                    values[self.grid[row_number][i].known - 1] = 1
                else:
                    print('There\'s a duplicate in row', row_number, 'you idiot. Try again.')
                    return False

        for i in range(len(values)):
            if values[i] == 1:
                self.row_options_update(row_number, i)

        return True

    def column_validate(self, column_number):
        """Checks if there are any duplicates in a given column, and updates empty square options."""
        values = [0 for i in range(self.length)]

        for i in range(self.length):
            if hasattr(self.grid[i][column_number], 'known'):
                if values[self.grid[i][column_number].known - 1] == 0:
                    values[self.grid[i][column_number].known - 1] = 1
                else:
                    print('There\'s a duplicate in column', column_number, 'you idiot. Try again.')
                    return False

        # Update list of options for empty squares
        for i in range(len(values)):
            if values[i] == 1:
                self.column_options_update(column_number, i)

        return True

    def box_validate(self, box_number):
        """Checks if there are any duplicates in a given box, and updates empty square options."""
        values = [0 for i in range(self.length)]
        # box_number = 3*math.floor(row_number) + math.floor(column_number)
        row_start = 3 * math.floor(box_number / 3)
        column_start = 3 * (box_number % 3)

        for i in range(row_start, row_start + 3):
            for j in range(column_start, column_start + 3):
                if hasattr(self.grid[i][j], 'known'):
                    if values[self.grid[i][j].known - 1] == 0:
                        values[self.grid[i][j].known - 1] = 1
                    else:
                        print('There\'s a duplicate in box', box_number, 'you idiot. Try again.')
                        return False

        # Update list of options for empty squares
        for i in range(self.length):
            if values[i] == 1:
                self.box_options_update(box_number, i)

        return True

    def grid_sweep(self):
        """Run box_check and element_options_check. If known was found, return True."""
        known_update = False
        for i in range(self.length):
            box_result = self.box_check(i)
            for j in range(self.length):
                element_options_result = self.element_options_check(i, j)
                if box_result or element_options_result:
                    known_update = True
        return known_update

    def box_check(self, box_number):
        """Check if, in a box, only one option appears. If so, set to known."""
        values = [0 for i in range(self.length)]
        row_start = 3 * math.floor(box_number / 3)
        column_start = 3 * (box_number % 3)

        for i in range(row_start, row_start + 3):
            for j in range(column_start, column_start + 3):
                if not hasattr(self.grid[i][j], 'known'):
                    for k in range(len(values)):
                        if self.grid[i][j].options[k] == 1:
                            values[k] += 1

        for i in range(len(values)):
            if values[i] == 1:
                for j in range(row_start, row_start + 3):
                    for k in range(column_start, column_start + 3):
                        if not hasattr(self.grid[j][k], 'known'):
                            if self.grid[j][k].options[i] == 1:
                                self.grid[j][k].known = self.grid[j][k].options[i] + 1
                                print('box check update')
                                return True

    def element_options_check(self, i, j):
        """Check if an element has only one possible option. If so, set it as known."""
        if not hasattr(self.grid[i][j], 'known'):
            if self.grid[i][j].options.count(1) == 1:
                self.grid[i][j].known = self.grid[i][j].options.index(1) + 1
                print('element check update')
                return True

    def row_options_update(self, row_number, value_index):
        """Remove invalid options determined via row rules."""
        for i in range(self.length):
            if hasattr(self.grid[row_number][i], 'options'):
                self.grid[row_number][i].options[value_index] = 0

    def column_options_update(self, column_number, value_index):
        """Remove invalid options determined via column rules."""
        for i in range(self.length):
            if hasattr(self.grid[i][column_number], 'options'):
                self.grid[i][column_number].options[value_index] = 0

    def box_options_update(self, box_number, value_index):
        """Remove invalid options determined via box rules."""
        row_start = 3 * math.floor(box_number / 3)
        column_start = 3 * (box_number % 3)
        for i in range(row_start, row_start + 3):
            for j in range(column_start, column_start + 3):
                if hasattr(self.grid[i][j], 'options'):
                    self.grid[i][j].options[value_index] = 0
