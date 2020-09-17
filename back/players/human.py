class Human:
    def __init__(self, map, log, side, friendly=()):
        self.map = map
        self.log = log
        self.side = side
        self.friendly = friendly

    def process_click(self, pos, ctrl):
        cursor, grid = ctrl.cursor, self.map.get_grid(pos)
        ctrl.cursor = grid
        if cursor is not None and grid is not None:
            # both are valid blocks
            block = self.map.board[cursor[0]][cursor[1]]
            if block.piece == self.side and grid in self.map.get_avail(cursor):
                self.map.move(cursor, grid, self.friendly)
                self.log.push(['move', cursor, grid])
                return 'next'

    def get_move(self):
        return None
