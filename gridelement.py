class GridElement:
    def __init__(self, element):
        if element == 0:
            self.options = [1 for i in range(9)]
        else:
            self.known = element
