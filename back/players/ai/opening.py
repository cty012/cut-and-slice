import random


class Opening:
    def __init__(self, mode, side):
        self.mode = mode
        self.side = side
        self.moves = [
            [((0, 0), (1, 0)), ((0, 0), (0, 2)), ((0, 1), (3, 1)), ((1, 1), (1, 5))],
            [((0, 0), (1, 0)), ((0, 0), (0, 2)), ((0, 1), (2, 2)), ((1, 2), (1, 6))],
            [((0, 0), (1, 0)), ((0, 0), (0, 2)), ((0, 1), (2, 2)), ((1, 1), (5, 1))],
            [((0, 0), (1, 0)), ((1, 0), (3, 0)), ((1, 0), (2, 2)), ((2, 1), (6, 1))],
            [((0, 0), (1, 0)), ((1, 0), (1, 2)), ((1, 0), (3, 1)), ((2, 1), (2, 5))],
        ]
        self.move = random.choices(
            population=self.moves,
            weights=[0.25, 0.125, 0.125, 0.25, 0.25]
        )[0]
        self.flip = random.random() < 0.5
        self.current = 0

    def get_move(self):
        move = self.move[self.current]
        if self.flip:
            # flip
            move = ((move[0][1], move[0][0]), (move[1][1], move[1][0]))
        # rotate for different colors
        if self.mode == '1':
            if self.side == 'red':
                move = ((move[0][0], 8 - move[0][1]), (move[1][0], 8 - move[1][1]))
            elif self.side == 'blue':
                move = ((8 - move[0][0], move[0][1]), (8 - move[1][0], move[1][1]))
        elif self.mode == '2':
            if self.side == 'red':
                move = ((move[0][0], 10 - move[0][1]), (move[1][0], 10 - move[1][1]))
            elif self.side == 'yellow':
                move = ((10 - move[0][0], 10 - move[0][1]), (10 - move[1][0], 10 - move[1][1]))
            elif self.side == 'green':
                move = ((10 - move[0][0], move[0][1]), (10 - move[1][0], move[1][1]))
        self.current += 1
        return ['move', move[0], move[1]]


### MOVES
## 1:
#       4
#       4
#       4
#   2   4
#   2   3   3   3
#   0   1
## 2:
#       4
#       4
#       4
#       4
#   2   3   3
#   2   3
#   0   1
## 3:
#   2   3   3
#   2   3   4   4   4   4
#   0   1
## 4:
#           3
#       3   3   4   4   4   4
#   0   1   2   2
## 5:
#           4
#           4
#           4
#       2   4
#       2   3   3
#   0   1   3
