class GridElement:
    """Information about squares on the grid to be solved."""
    def __init__(self, element, box_size):
        if element == 0:
            self.options = [1 for i in range(box_size*box_size)]
            self.original = False
        else:
            self.known = element
            self.original = True
