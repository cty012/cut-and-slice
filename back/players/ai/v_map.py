import random
import utils.functions as utils


class VMap:
    def __init__(self, board):
        self.board = board
        self.size = len(board), len(board[0])
        # cover, all moves, and value
        self.cover = 0
        rand = 0.5 * (random.random() - 0.5)
        self.values = {'red': rand, 'blue': -rand}
        self.all_moves = None
        self.get_all_moves()
        self.get_values()

    def clone(self):
        board = [[self.board[i][j] for j in range(self.size[1])] for i in range(self.size[0])]
        return VMap(board)

    def move(self, base, target, friendly=()):
        other = self.clone()
        for between in utils.get_between(base, target):
            if other.board[between[0]][between[1]] not in friendly:
                other.board[between[0]][between[1]] = self.board[base[0]][base[1]]
        return other

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

    def cover_rate(self):
        return self.cover / (self.size[0] * self.size[1])

    def get_all_moves(self):
        self.cover, self.all_moves = 0, {'red': [], 'blue': []}
        cut_value = [[0 for j in range(self.size[1])] for i in range(self.size[0])]
        # calc all moves and cover
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.board[i][j] is not None:
                    side = self.board[i][j]
                    opponent = {'red': 'blue', 'blue': 'red'}[side]
                    self.cover += 1
                    for target in self.get_avail((i, j)):
                        self.all_moves[side].append([(i, j), target])
                        between = utils.get_between((i, j), target)
                        for each in between:
                            if self.board[each[0]][each[1]] == opponent:
                                cut_value[each[0]][each[1]] += 1
        # calc cut value
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if cut_value[i][j] > 0:
                    side = self.board[i][j]
                    if side == 'red':
                        value = 0.2 * (8 - i) + 0.2 * j - 0.6
                    else:
                        value = 0.2 * (8 - j) + 0.2 * i - 0.6
                    self.values[side] -= value

    def get_values(self):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                piece = self.board[i][j]
                # calc 2x2 block value
                if piece is not None and i < self.size[0] - 1 and j < self.size[1] - 1:
                    if self.board[i + 1][j] == piece and self.board[i][j + 1] == piece and self.board[i + 1][j + 1] == piece:
                        self.values[piece] += 1.0
                # calc piece value
                value = 6.0 - 0.25 * abs(i - 4) - 0.25 * abs(j - 4)
                if piece == 'red':
                    self.values['red'] += (value + 0.1 * self.get_power((i, j)))
                elif piece == 'blue':
                    self.values['blue'] += (value + 0.1 * self.get_power((i, j)))
        # calc blank value
        blank_value = [[{'red': 0, 'blue': 0} for j in range(self.size[1])] for i in range(self.size[0])]
        for power in (4, 3, 2, 1):
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    side = self.board[i][j]
                    if side is not None and self.get_power((i, j)) == power:
                        blank_value[i][j][side] = max(blank_value[i][j][side], power)
        weight = -0.2 + 0.8 * self.cover_rate()
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if blank_value[i][j]['red'] > 0 and blank_value[i][j]['blue'] == 0:
                    self.values['red'] += weight
                elif blank_value[i][j]['red'] == 0 and blank_value[i][j]['blue'] > 0:
                    self.values['blue'] += weight

    def evaluate(self, side):
        opponent = {'red': 'blue', 'blue': 'red'}[side]
        return self.values[side] - self.values[opponent]
