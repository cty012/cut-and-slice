import back.sprites.component as c


class Scene:
    def __init__(self, args, mode):
        self.args = args
        self.mode = mode
        self.threshold = 42
        self.pos = (0, 0)
        self.background = c.Component(lambda ui: ui.show_div((0, 0), self.args.size, color=(60, 179, 113)))
        self.buttons = {
            'p1': c.Button((self.args.size[0] // 2 - 280, 260), (360, 180), 'Human',
                           font=('src', 'timesnewroman.ttf', 30), align=(1, 1), background=(255, 204, 204)),
            'p2': c.Button((self.args.size[0] // 2 + 280, 260), (360, 180), 'Human',
                           font=('src', 'timesnewroman.ttf', 30), align=(1, 1), background=(204, 204, 255)),
            '-': c.Button((self.args.size[0] // 2 - 300, 460), (50, 70), '',
                          font=('src', 'timesnewroman.ttf', 25), align=(0, 1), background=(210, 210, 210)),
            'threshold': c.Button((self.args.size[0] // 2, 460), (470, 70), f'Red\'s winning threshold: {self.threshold}',
                                  font=('src', 'timesnewroman.ttf', 22), align=(1, 1), background=(210, 210, 210)),
            '+': c.Button((self.args.size[0] // 2 + 300, 460), (50, 70), '',
                          font=('src', 'timesnewroman.ttf', 25), align=(2, 1), background=(210, 210, 210)),
            'play': c.Button((self.args.size[0] // 2, 550), (600, 70), 'Play',
                             font=('src', 'timesnewroman.ttf', 25), align=(1, 1), background=(210, 210, 210)),
            'back': c.Button((self.args.size[0] // 2, 640), (600, 70), 'Back',
                             font=('src', 'timesnewroman.ttf', 25), align=(1, 1), background=(210, 210, 210)),
        }

    def process_events(self, events):
        if events['mouse-left'] == 'down':
            for name in self.buttons:
                if self.buttons[name].in_range(events['mouse-pos']):
                    return self.execute(name)
        return [None]

    def execute(self, name):
        if name in ['p1', 'p2']:
            button = self.buttons[name]
            button.text = {'Human': 'AI', 'AI': 'Human'}[button.text]
        elif name == '+':
            self.threshold += 1
            self.threshold = min(self.threshold, 80)
            self.buttons['threshold'].text = f'Red\'s winning threshold: {self.threshold}'
        elif name == '-':
            self.threshold -= 1
            self.threshold = max(self.threshold, 1)
            self.buttons['threshold'].text = f'Red\'s winning threshold: {self.threshold}'
        elif name == 'play':
            player_mode = []
            for p in ['p1', 'p2']:
                player_mode.append('p' if self.buttons[p].text == 'Human' else 'c')
            return ['game', self.mode, 'v'.join(player_mode), self.threshold]
        elif name == 'back':
            return ['mode']
        return [None]

    def show(self, ui):
        self.background.show(ui)
        ui.show_text((self.args.size[0] // 2, 80), "Game Settings", font=('src', 'cambria.ttf', 60), align=(1, 1))
        ui.show_text((self.args.size[0] // 2, 260), "VS", font=('src', 'cambria.ttf', 60), align=(1, 1))
        for name in self.buttons:
            self.buttons[name].show(ui)
        ui.show_triangle((self.args.size[0] // 2 - 275, 460), 6, 'left')
        ui.show_triangle((self.args.size[0] // 2 + 275, 460), 6, 'right')
