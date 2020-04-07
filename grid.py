import math
from gridelement import GridElement


class Grid:
    def __init__(self, init_data, box_size):
        self.valid = True
        self.length = len(init_data)
        self.box_size = box_size
        self.grid = [[GridElement(init_data[j][i], self.box_size) for i in range(self.length)] for j in range(self.length)]

    def row_validate(self, row_number):
        """Checks if there are any duplicates in a given row, and updates empty square options."""
        values = [0 for i in range(self.length)]

        # Check for duplicates
        for i in range(self.length):
            if hasattr(self.grid[row_number][i], 'known'):
                if values[self.grid[row_number][i].known - 1] == 0:
                    values[self.grid[row_number][i].known - 1] = 1
                else:
                    print('There\'s a duplicate in row', row_number, 'you idiot. Try again.')
                    return False

        # Update empty square options
        for i in range(len(values)):
            if values[i] == 1:
                self.row_options_update(row_number, i)

        return True

    def column_validate(self, column_number):
        """Checks if there are any duplicates in a given column, and updates empty square options."""
        values = [0 for i in range(self.length)]

        # Check for duplicates
        for i in range(self.length):
            if hasattr(self.grid[i][column_number], 'known'):
                if values[self.grid[i][column_number].known - 1] == 0:
                    values[self.grid[i][column_number].known - 1] = 1
                else:
                    print('There\'s a duplicate in column', column_number, 'you idiot. Try again.')
                    return False

        # Update empty square options
        for i in range(len(values)):
            if values[i] == 1:
                self.column_options_update(column_number, i)

        return True

    def box_validate(self, box_number):
        """Checks if there are any duplicates in a given box, and updates empty square options."""
        values = [0 for i in range(self.length)]
        row_start = self.box_size * math.floor(box_number / self.box_size)
        column_start = self.box_size * (box_number % self.box_size)

        for i in range(row_start, row_start + self.box_size):
            for j in range(column_start, column_start + self.box_size):
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

    def grid_validate(self):
        print('Validating grid...')
        for i in range(self.length):
            result_row = self.row_validate(i)
            result_column = self.column_validate(i)
            result_box = self.box_validate(i)
            if not result_row or not result_column or not result_box:
                print('Invalid initial grid!')
                return False
        print('Grid valid')
        return True

    def grid_sweep(self):
        """See if we can remove some options from empty squares. Then check if we can set anything to known. If known was found, return True."""
        known_update = False

        # for i in range(self.length):
        #    self.box_row_simplify(i)
        #    self.box_column_simplify(i)

        for i in range(self.length):
            row_result = self.row_check(i)
            column_result = self.column_check(i)
        for i in range(self.length):
            box_result = self.box_check(i)

        el_res_count = 0
        for i in range(self.length):
            for j in range(self.length):
                el_res_count += self.element_check(i, j)

        return row_result or column_result or box_result or el_res_count

    def box_row_simplify(self, box_number):
        """If an option only appears in a single row within a box,
        remove that option from other empty squares in that "global" row."""
        values = [0 for i in range(self.length)]
        row_flag = [0 for i in range(self.box_size)]
        row_start = self.box_size * math.floor(box_number / self.box_size)
        column_start = self.box_size * (box_number % self.box_size)

        for i in range(len(values)):
            for j in range(row_start, row_start + self.box_size):
                for k in range(column_start, column_start + self.box_size):
                    if not hasattr(self.grid[j][k], 'known'):
                        if self.grid[j][k].options[i] == 1:
                            values[i] += 1
                if values[i] > 1:
                    row_flag[j-row_start] = 1
                values[i] = 0
            if row_flag.count(1) == 1:
                row_number = row_flag.index(1) + row_start
                for j in range(self.length):
                    if not hasattr(self.grid[row_number][j], 'known') and not row_start <= j <= (row_start + self.box_size):
                        self.grid[row_number][j].options[i] = 0

    def box_column_simplify(self, box_number):
        """If an option only appears in a single column within a box,
        remove that option from other empty squares in that "global" column."""
        values = [0 for i in range(self.length)]
        column_flag = [0 for i in range(self.box_size)]
        row_start = self.box_size * math.floor(box_number / self.box_size)
        column_start = self.box_size * (box_number % self.box_size)

        for i in range(len(values)):
            for j in range(column_start, column_start + self.box_size):
                for k in range(row_start, row_start + self.box_size):
                    if not hasattr(self.grid[j][k], 'known'):
                        if self.grid[j][k].options[i] == 1:
                            values[i] += 1
                if values[i] > 1:
                    column_flag[j-column_start] = 1
                values[i] = 0
            if column_flag.count(1) == 1:
                column_number = column_flag.index(1)+column_start
                for j in range(self.length):
                    if not hasattr(self.grid[j][column_number], 'known') and not column_start <= j <= (column_start + self.box_size):
                        self.grid[j][column_number].options[i] = 0

    def box_check(self, box_number):
        """Check if, in a box, only one option appears. If so, set to known."""
        values = [0 for i in range(self.length)]
        row_start = self.box_size * math.floor(box_number / self.box_size)
        column_start = self.box_size * (box_number % self.box_size)

        for i in range(len(values)):
            for j in range(row_start, row_start + self.box_size):
                for k in range(column_start, column_start + self.box_size):
                    if not hasattr(self.grid[j][k], 'known'):
                        if self.grid[j][k].options[i] == 1:
                            values[i] += 1

        for i in range(len(values)):
            if values[i] == 1:
                for j in range(row_start, row_start + self.box_size):
                    for k in range(column_start, column_start + self.box_size):
                        if not hasattr(self.grid[j][k], 'known'):
                            if self.grid[j][k].options[i] == 1:
                                self.grid[j][k].known = i + 1
                                self.row_options_update(j, i)
                                self.column_options_update(k, i)
                                return True

    def row_check(self, row_number):
        """Check if an option appears only once in a given row. If so, set to known."""
        values = [0 for i in range(self.length)]
        known_flag = False

        for i in range(len(values)):
            for j in range(self.length):
                if not hasattr(self.grid[row_number][j], 'known'):
                    if self.grid[row_number][j].options[i] == 1:
                        values[i] += 1

        for i in range(len(values)):
            if values[i] == 1:
                for j in range(self.length):
                    if not hasattr(self.grid[row_number][j], 'known'):
                        if self.grid[row_number][j].options[i] == 1:
                            self.grid[row_number][j].known = i + 1
                            self.column_options_update(j, i)
                            box_number = self.box_size * math.floor(row_number / self.box_size) \
                                        + math.floor(j / self.box_size)
                            self.box_options_update(box_number, i)
                            known_flag = True

        return known_flag

    def column_check(self, column_number):
        """Check if an option appears only once in a given column. If so, set to known."""
        values = [0 for i in range(self.length)]
        known_flag = False

        for i in range(len(values)):
            for j in range(self.length):
                if not hasattr(self.grid[j][column_number], 'known'):
                    if self.grid[j][column_number].options[i] == 1:
                        values[i] += 1

        for i in range(len(values)):
            if values[i] == 1:
                for j in range(self.length):
                    if not hasattr(self.grid[j][column_number], 'known'):
                        if self.grid[j][column_number].options[i] == 1:
                            self.grid[j][column_number].known = i + 1
                            self.row_options_update(j, i)
                            box_number = self.box_size * math.floor(j / self.box_size) \
                                         + math.floor(column_number / self.box_size)
                            self.box_options_update(box_number, i)
                            known_flag = True

        return known_flag

    def element_check(self, i, j):
        """Check if an element has only one possible option. If so, set it as known."""
        if not hasattr(self.grid[i][j], 'known'):
            if self.grid[i][j].options.count(1) == 1:
                value_index = self.grid[i][j].options.index(1)
                self.grid[i][j].known = value_index + 1
                self.row_options_update(i, value_index)
                self.column_options_update(j, value_index)
                box_number = self.box_size * math.floor(i / self.box_size) \
                             + math.floor(j / self.box_size)
                self.box_options_update(box_number, value_index)
                return True
        return False

    def row_options_update(self, row_number, value_index):
        """Remove invalid options determined via row rules."""
        for i in range(self.length):
            if not hasattr(self.grid[row_number][i], 'known'):
                self.grid[row_number][i].options[value_index] = 0

    def column_options_update(self, column_number, value_index):
        """Remove invalid options determined via column rules."""
        for i in range(self.length):
            if not hasattr(self.grid[i][column_number], 'known'):
                self.grid[i][column_number].options[value_index] = 0

    def box_options_update(self, box_number, value_index):
        """Remove invalid options determined via box rules."""
        row_start = self.box_size * math.floor(box_number / self.box_size)
        column_start = self.box_size * (box_number % self.box_size)
        for i in range(row_start, row_start + self.box_size):
            for j in range(column_start, column_start + self.box_size):
                if not hasattr(self.grid[i][j], 'known'):
                    self.grid[i][j].options[value_index] = 0

    def row_check_update(self, row_number, column_number, value_index):
        for i in range(self.length):
            if not i == column_number and not hasattr(self.grid[row_number][i], 'known'):
                self.grid[row_number][i].options[value_index] == 0

    def column_check_update(self, row_number, column_number, value_index):
        for i in range(self.length):
            if not i == row_number and not hasattr(self.grid[i][column_number], 'known'):
                self.grid[i][column_number].options[value_index] == 0

    def box_check_update(self, row_number, column_number, value_index):
        box_number = self.box_size * math.floor(row_number/self.box_size) + math.floor(column_number/self.box_size)
        row_start = self.box_size * math.floor(box_number / self.box_size)
        column_start = self.box_size * (box_number % self.box_size)

        for i in range(row_start, row_start + self.box_size):
            for j in range(column_start, column_start + self.box_size):
                if not i == row_number and not j == column_number and not hasattr(self.grid[i][j], 'known'):
                    self.grid[i][j].options[value_index] = 0
