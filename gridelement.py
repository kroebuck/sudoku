class GridElement:
    def __init__(self, element, box_size):
        if element == 0:
            self.options = [1 for i in range(box_size*box_size)]
        else:
            self.known = element
