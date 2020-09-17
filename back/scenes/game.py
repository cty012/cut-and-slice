import back.sprites.component as c
import back.sprites.game as g
import back.sprites.replay as r
import back.sprites.saver as s


class Scene:
    def __init__(self, args, mode, player_mode, threshold, file=None):
        self.args = args
        self.pos = (0, 0)
        self.background = c.Component(lambda ui: ui.show_div((0, 0), self.args.size, color=(60, 179, 113)))
        # game
        self.mode = None
        self.player_mode = player_mode
        self.game = None
        if mode in ['1', '2']:
            self.mode = mode
            self.game = g.Game(self.args, self.mode, self.player_mode, threshold)
            self.game.prepare()
        elif mode == 'save':
            self.mode = file.mode
            self.game = file
        elif mode == 'replay':
            self.mode = file.mode
            self.game = r.Replay(self.args, self.mode, self.player_mode, threshold)
            self.game.prepare(log=file)
        self.saver = s.Saver(self.args, msg=self.game.name)

    def process_events(self, events):
        if self.saver.active:
            return self.execute(self.saver.process_events(events))
        for key in events['key-pressed']:
            if key == 'w':
                self.game.move((0, 10))
            elif key == 'a':
                self.game.move((10, 0))
            elif key == 's':
                self.game.move((0, -10))
            elif key == 'd':
                self.game.move((-10, 0))
        return self.execute(self.game.process_events(events))

    def execute(self, name):
        if name == 'save':
            self.saver.activate(self.game.name)
        elif name == 'save_game':
            self.saver.save(self.game)
        elif name == 'quit':
            return ['menu']
        return [None]

    def show(self, ui):
        self.background.show(ui)
        self.game.show(ui)
        if self.saver.active:
            self.saver.show(ui)
