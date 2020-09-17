import utils.functions as utils


class Controls:
    def __init__(self, map):
        self.map = map
        self.cursor = None
        self.between = []

    def process_hover(self, pos):
        grid = self.map.get_grid(pos)
        self.between = []
        if self.cursor is not None and grid is not None and grid in self.map.get_avail(self.cursor):
            self.between = utils.get_between(self.cursor, grid)
