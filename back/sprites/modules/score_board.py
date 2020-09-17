import utils.functions as utils


class ScoreBoard:
    def __init__(self, mode, map, threshold, pos, *, align=(0, 0)):
        # display
        self.size = {'1': (180, 180), '2': (180, 250)}[mode]
        self.pos = utils.top_left(pos, self.size, align=align)
        # game
        self.mode = mode
        self.map = map
        self.threshold = threshold
        self.sides = ['red', 'blue'] if self.mode == '1' else ['red', 'yellow', 'blue', 'green']
        self.colors = {'red': (255, 0, 0), 'yellow': (204, 204, 0), 'blue': (0, 0, 255), 'green': (0, 255, 0)}

    def in_range(self, pos):
        return self.pos[0] < pos[0] < self.pos[0] + self.size[0] and self.pos[1] < pos[1] < self.pos[1] + self.size[1]

    def get_scores(self):
        scores = [0] * len(self.sides)
        for i in range(len(self.map.board)):
            for j in range(len(self.map.board[0])):
                block = self.map.board[i][j]
                if block.piece is not None:
                    scores[self.sides.index(block.piece)] += 1
        return scores

    def get_winner(self):
        scores = self.get_scores()
        if self.mode == '1' and sum(scores) == 81:
            return ['red'] if scores[0] >= self.threshold else ['blue']
        elif self.mode == '2' and sum(scores) == 121:
            return ['red', 'green'] if scores[0] + scores[3] >= self.threshold else ['yellow', 'blue']
        return []

    def show(self, ui, *, pan=(0, 0)):
        pos = self.pos[0] + pan[0], self.pos[1] + pan[1]
        # container
        ui.show_div(pos, self.size, color=(255, 255, 255))
        ui.show_div(pos, self.size, border=2)
        # title
        ui.show_text((self.size[0] // 2, 20), 'Scores:', ('src', 'timesnewroman.ttf', 25), align=(1, 0), pan=pos)
        # scores
        scores = self.get_scores()
        ui.show_text((30, 60), f'Threshold: {self.threshold}', ('src', 'timesnewroman.ttf', 20), align=(0, 0), pan=pos)
        for i, side in enumerate(self.sides):
            ui.show_text((30, 95 + i * 35), f'{side.capitalize()}: {scores[i]}',
                         ('src', 'timesnewroman.ttf', 20), color=self.colors[side], align=(0, 0), pan=pos)
