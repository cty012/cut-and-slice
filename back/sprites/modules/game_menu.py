import back.sprites.component as c
import utils.functions as utils


class GameMenu:
    def __init__(self, mode, pos, *, buttons=('save', 'quit'), size=(200, 220), align=(0, 0)):
        # display
        self.pos = utils.top_left(pos, size, align=align)
        self.size = size
        # game
        self.mode = mode
        self.round = 1
        self.sides = ['red', 'blue'] if self.mode == '1' else ['red', 'yellow', 'blue', 'green']
        self.colors = {'red': (255, 0, 0), 'yellow': (204, 204, 0), 'blue': (0, 0, 255), 'green': (0, 255, 0)}
        self.current = 0
        self.winner = []
        # buttons
        self.buttons = {
            buttons[0]: c.Button((self.pos[0] + self.size[0] // 2, self.pos[1] + 110), (150, 40),
                          buttons[0], font=('src', 'timesnewroman.ttf', 22), align=(1, 0), background=(230, 230, 230)),
            buttons[1]: c.Button((self.pos[0] + self.size[0] // 2, self.pos[1] + 160), (150, 40),
                          buttons[1], font=('src', 'timesnewroman.ttf', 22), align=(1, 0), background=(230, 230, 230)),
        }

    def in_range(self, pos):
        return self.pos[0] < pos[0] < self.pos[0] + self.size[0] and self.pos[1] < pos[1] < self.pos[1] + self.size[1]

    def side(self):
        return self.sides[self.current]

    def process_click(self, pos):
        # buttons
        for name in self.buttons:
            if self.buttons[name].in_range(pos):
                return self.buttons[name].text

    def next(self):
        self.current = (self.current + 1) % len(self.sides)
        if self.current == 0:
            self.round += 1

    def show(self, ui, *, pan=(0, 0)):
        pos = self.pos[0] + pan[0], self.pos[1] + pan[1]
        # container
        ui.show_div(pos, self.size, color=(255, 255, 255))
        ui.show_div(pos, self.size, border=2)
        # round
        ui.show_text((self.size[0] // 2, 20), f'ROUND {self.round}',
                     ('src', 'timesnewroman.ttf', 25), align=(1, 0), pan=pos)
        # current player or winner
        if len(self.winner) == 0:
            ui.show_text((self.size[0] // 2, 65), f'{self.side().capitalize()}\'s turn', ('src', 'timesnewroman.ttf', 22),
                         color=self.colors[self.sides[self.current]], align=(1, 0), pan=pos)
        else:
            texts = []
            for winner in self.winner:
                texts += [[winner.capitalize(), self.colors[winner]], [' & ', (0, 0, 0)]]
            texts = texts[:-1] + [[' wins!', (0, 0, 0)]]
            ui.show_texts((self.size[0] // 2, 65), texts, ('src', 'timesnewroman.ttf', 22), align=(1, 0), pan=pos)
        # buttons
        for name in self.buttons:
            self.buttons[name].show(ui)
