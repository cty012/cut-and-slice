import utils.functions as utils


class VMap:
    def __init__(self, mode, board, nn):
        self.mode = mode
        self.board = board
        self.size = len(board), len(board[0])
        # evaluation function
        self.nn = nn
        factor = 1
        self.eval_func = lambda side, friendly:\
            self.nn.forward(self.state(side, friendly)) + factor * (2 * self.count([side] + friendly) - self.cover())

    def clone(self):
        board = [[self.board[i][j] for j in range(self.size[1])] for i in range(self.size[0])]
        return VMap(self.mode, board, self.nn)

    def count(self, pieces):
        total = 0
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.board[i][j] in pieces:
                    total += 1
        return total

    def cover(self):
        cover = 0
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.board[i][j] is not None:
                    cover += 1
        return cover

    def cover_rate(self):
        return self.cover() / (self.size[0] * self.size[1])

    def move(self, base, target, friendly=()):
        other = self.clone()
        for between in utils.get_between(base, target):
            if other.board[between[0]][between[1]] not in friendly:
                other.board[between[0]][between[1]] = self.board[base[0]][base[1]]
        return other

    def state(self, side, friendly=[], ignore=[None]):
        ans = []
        count = 0
        for row in self.board:
            for element in row:
                if element == side or element in friendly:
                    count += 1
                    ans.append(1.0)
                    ans.append(0.0)
                    ans.append(0.0)
                elif element in ignore:
                    ans.append(0.0)
                    ans.append(1.0)
                    ans.append(0.0)
                else:
                    ans.append(0.0)
                    ans.append(0.0)
                    ans.append(1.0)
        return ans

    def get_power(self, pos):
        (x, y) = pos
        return min(len([
            p for p in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            if 0 <= p[0] < self.size[0] and 0 <= p[1] < self.size[1] and
               self.board[x][y] == self.board[p[0]][p[1]]
        ]) + 1, 4)

    def get_avail(self, pos):
        ans = []
        if self.board[pos[0]][pos[1]] is not None:
            power = self.get_power(pos)
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    if utils.get_dist(pos, (i, j)) <= power and self.board[i][j] is None:
                        ans.append((i, j))
        return ans

    def get_all_moves(self, side):
        all_moves = []
        # calc all moves
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.board[i][j] == side:
                    for target in self.get_avail((i, j)):
                        all_moves.append([(i, j), target])
        return all_moves

    def evaluate(self, side, friendly):
        return self.eval_func(side, friendly)
