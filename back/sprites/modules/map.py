import utils.functions as utils


class Block:
    def __init__(self, pos, size, *, align=(0, 0)):
        self.piece = None
        self.pos = utils.top_left(pos, (size, size), align=align)
        self.size = size

    def in_range(self, pos, *, pan=(0, 0)):
        abs_pos = (self.pos[0] + pan[0], self.pos[1] + pan[1])
        return abs_pos[0] < pos[0] < abs_pos[0] + self.size and abs_pos[1] < pos[1] < abs_pos[1] + self.size

    def show(self, ui, *, b_color=(255, 255, 255), is_avail=False, pan=(0, 0)):
        center = self.pos[0] + self.size // 2, self.pos[1] + self.size // 2
        # show background
        ui.show_div(self.pos, (self.size, self.size), color=b_color, pan=pan)
        # show image
        if self.piece is not None:
            ui.show_img(center, self.piece + '.png', align=(1, 1), pan=pan)
        if is_avail:
            ui.show_img(center, 'available.png', align=(1, 1), pan=pan)


class Map:
    def __init__(self, mode, pos, *, align=(0, 0)):
        self.mode = mode
        self.size = (9, 9) if self.mode == '1' else (11, 11)
        self.block_size = 70
        self.total_size = (self.size[0] * self.block_size, self.size[1] * self.block_size)
        self.pos = utils.top_left(pos, self.total_size, align=align)
        # board
        self.board = None
        self._board = None
        self.prepare()

    def prepare(self):
        self.board = [[Block((i * self.block_size, j * self.block_size), self.block_size)
                       for j in range(self.size[1])] for i in range(self.size[0])]
        self._board = [[None for j in range(self.size[1])] for i in range(self.size[0])]
        MapLoader.init(self, self.mode)
        MapLoader.save(self.board, self._board)

    def move(self, base, target, friendly=()):
        for between in utils.get_between(base, target):
            block = self.board[between[0]][between[1]]
            if block.piece not in friendly:
                block.piece = self.board[base[0]][base[1]].piece

    def in_range(self, pos):
        return self.pos[0] < pos[0] < self.pos[0] + self.total_size[0] and \
               self.pos[1] < pos[1] < self.pos[1] + self.total_size[1]

    def get_grid(self, pos):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.board[i][j].in_range(pos, pan=self.pos):
                    return i, j
        return None

    def get_avail(self, pos):
        (x, y), block = pos, self.board[pos[0]][pos[1]]
        ans = []
        if block.piece is not None:
            adj = min(len([
                p for p in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                if 0 <= p[0] < self.size[0] and 0 <= p[1] < self.size[1] and block.piece == self.board[p[0]][p[1]].piece
            ]) + 1, 4)
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    if utils.get_dist(pos, (i, j)) <= adj and self.board[i][j].piece is None:
                        ans.append((i, j))
        return ans

    def get_status(self, pos, cursor, between, side):
        color = (255, 255, 255)
        avail = False
        # show cursor
        if pos == cursor:
            color = (230, 230, 230)
        if cursor is not None and self.board[cursor[0]][cursor[1]].piece == side:
            # show between
            if pos in between:
                color = {
                    'red': (255, 230, 230), 'blue': (230, 230, 255),
                    'yellow': (255, 255, 230), 'green': (230, 255, 230)
                }.get(side, color)
            # show avail
            avail = pos in self.get_avail(cursor)
        return color, avail

    def show(self, ui, cursor=None, between=(), side=None):
        # show blocks
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                color, avail = self.get_status((i, j), cursor, between, side)
                self.board[i][j].show(ui, b_color=color, is_avail=avail, pan=self.pos)
        # show borders
        for i in range(self.size[0] + 1):
            start = (self.pos[0], self.pos[1] + i * self.block_size)
            end = (self.pos[0] + self.size[1] * self.block_size, self.pos[1] + i * self.block_size)
            ui.show_line(start, end)
        for i in range(self.size[1] + 1):
            start = (self.pos[0] + i * self.block_size, self.pos[1])
            end = (self.pos[0] + i * self.block_size, self.pos[1] + self.size[0] * self.block_size)
            ui.show_line(start, end)


class MapLoader:
    @classmethod
    def init(cls, map, mode):
        if mode == '1':
            cls.load(
                map.board,
                [[None] * 8 + ['red']] +
                [[None] * 9] * 7 +
                [['blue'] + [None] * 8]
            )
        elif mode == '2':
            cls.load(
                map.board,
                [['blue'] + [None] * 9 + ['red']] +
                [[None] * 11] * 9 +
                [['green'] + [None] * 9 + ['yellow']]
            )

    @classmethod
    def load(cls, board, _board):
        for i in range(len(board)):
            for j in range(len(board[0])):
                board[i][j].piece = _board[i][j]

    @classmethod
    def save(cls, board, _board):
        for i in range(len(board)):
            for j in range(len(board[0])):
                _board[i][j] = board[i][j].piece
