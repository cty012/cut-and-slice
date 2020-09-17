import back.sprites.game as g
import back.sprites.modules.controls as c
import back.sprites.modules.game_buttons as gb
import back.sprites.modules.game_menu as gm
import back.sprites.modules.map as m
import back.sprites.modules.score_board as sb
import back.players.replay_bot as rb


class Replay(g.Game):
    def __init__(self, args, mode, player_mode, threshold):
        self.bot = None
        super().__init__(args, mode, player_mode, threshold)

    def prepare(self, log=None):
        self.log = log
        self.map = m.Map(self.mode, (self.args.size[0] // 2, self.args.size[1] // 2), align=(1, 1))
        self.ctrl = c.Controls(self.map)
        self.game_menu = gm.GameMenu(self.mode, (self.args.size[0] - 15, 15), buttons=('play', 'quit'), align=(2, 0))
        self.game_buttons = gb.ReplaySpeed((self.args.size[0] - 15, self.args.size[1] - 15), align=(2, 2))
        self.score_board = sb.ScoreBoard(self.mode, self.map, self.threshold, (15, 15), align=(0, 0))
        self.bot = rb.ReplayBot(self.map, log)
        self.players = [self.bot for _ in self.game_menu.sides]

    def execute(self, name):
        if name == 'play':
            if not self.bot.stopwatch.is_running():
                self.bot.stopwatch.start(self.bot.speed)
            self.game_menu.buttons['play'].text = 'pause'
        elif name == 'pause':
            if self.bot.stopwatch.is_running():
                self.bot.stopwatch.stop()
            self.game_menu.buttons['play'].text = 'play'
        elif name == 'end':
            if self.bot.stopwatch.is_running():
                self.bot.stopwatch.stop()
            self.game_menu.buttons['play'].text = 'replay'
        elif name == 'replay':
            self.prepare(self.log)
            self.execute('play')
        elif name == 'speed+':
            speed = min(self.bot.speed * 2, 4)
            self.bot.speed = speed
            self.bot.stopwatch.set_speed(speed)
            self.game_buttons.buttons[''].text = f'speed×{speed}'
        elif name == 'speed-':
            speed = max(self.bot.speed // 2, 1)
            self.bot.speed = speed
            self.bot.stopwatch.set_speed(speed)
            self.game_buttons.buttons[''].text = f'speed×{speed}'
        elif name == 'quit':
            return 'quit'
        elif name == 'next':
            self.game_menu.winner = self.score_board.get_winner()
            if len(self.game_menu.winner) == 0:
                self.game_menu.next()
            else:
                self.execute('end')
