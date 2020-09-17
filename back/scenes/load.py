import os

import back.sprites.saver as s
import back.sprites.component as c
import utils.functions as utils


class Scene:
    def __init__(self, args, mode):
        self.args = args
        self.bar_height = 100
        self.mode = mode
        self.margin = 40
        self.padding = 20
        self.background = c.Component(lambda ui: ui.show_div((0, 0), self.args.size, color=(60, 179, 113)))
        self.saves = [SavedFile(file[:file.index('.')], self.mode, (800, 120))
                      for file in os.listdir(os.path.join('.', self.mode))
                      if file.endswith('.cns' if self.mode == 'save' else '.cnsr')]
        self.pan = 0
        self.button = c.Button((self.args.size[0] // 2, self.args.size[1] - self.bar_height // 2), (200, 50), 'back',
                               font=('src', 'timesnewroman.ttf', 22), align=(1, 1), background=(210, 210, 210))

    def process_events(self, events):
        total_height = len(self.saves) * (self.padding + 120) - self.padding + 2 * self.margin
        if events['mouse-left'] == 'down':
            m_pos = events['mouse-pos']
            # back button
            if m_pos[1] >= self.args.size[1] - self.bar_height:
                if self.button.in_range(m_pos):
                    return ['menu']
            # saved files
            else:
                for i, saved_file in enumerate(self.saves):
                    pos = (self.args.size[0] // 2, self.margin + i * (self.padding + saved_file.size[1]) + self.pan)
                    if saved_file.in_range(pos, m_pos, align=(1, 0)):
                        return self.execute(saved_file.process_click(pos, m_pos, align=(1, 0)))
        elif events['mouse-wheel'] == 'up':
            self.pan += 30
            self.pan = min(self.pan, 0)
        elif events['mouse-wheel'] == 'down' and total_height > self.args.size[1] - self.bar_height:
            self.pan -= 30
            self.pan = max(self.pan, self.args.size[1] - self.bar_height - total_height)
        return [None]

    def execute(self, command):
        if command[0] == 'delete':
            ext = '.cns' if self.mode == 'save' else '.cnsr'
            os.remove(os.path.join('.', command[1], command[2] + ext))
            for i in range(len(self.saves)):
                if self.saves[i].name == command[2]:
                    self.saves.pop(i)
                    break
        return command

    def show(self, ui):
        # background
        self.background.show(ui)
        # saves
        for i, saved_file in enumerate(self.saves):
            saved_file.show(ui, (self.args.size[0] // 2, self.margin + i * (self.padding + saved_file.size[1])),
                            align=(1, 0), pan=(0, self.pan))
        # bar
        ui.show_div((0, self.args.size[1]), (self.args.size[0], self.bar_height), color=(46, 139, 87), align=(0, 2))
        ui.show_line((0, self.args.size[1] - self.bar_height), (self.args.size[0], self.args.size[1] - self.bar_height),
                     width=2)
        # button
        self.button.show(ui)


class SavedFile:
    def __init__(self, name, mode, size, *, color=(210, 210, 210)):
        # display
        self.name = name
        self.mode = mode
        self.size = size
        self.player_colors = [(255, 204, 204), (255, 255, 204), (204, 204, 255), (204, 255, 204), (240, 240, 240)]
        self.side_colors = {
            'Red': [(255, 204, 204), (255, 204, 204)],
            'Yellow': [(255, 255, 204), (255, 255, 204)],
            'Blue': [(204, 204, 255), (204, 204, 255)],
            'Green': [(204, 255, 204), (204, 255, 204)],
            'Red & Green': [(255, 204, 204), (204, 255, 204)],
            'Yellow & Blue': [(255, 255, 204), (204, 204, 255)],
        }
        self.color = [color, color, color]
        # game
        self.game = None
        self.game_mode = None
        self.player_mode = None
        self.round = None
        self.side = None
        self.err = False
        try:
            if self.mode == 'save':
                self.game = s.Saver.load(self.name, self.mode)
                self.game_mode = self.game.mode
                self.player_mode = self.game.player_mode
                self.threshold = self.game.threshold
                self.round = self.game.game_menu.round
                self.side = self.game.game_menu.side().capitalize()

            elif self.mode == 'replay':
                # game = log
                self.game = s.Saver.load(self.name, self.mode)
                self.game_mode = self.game.mode
                self.player_mode = self.game.player_mode
                self.threshold = self.game.threshold
                self.round = (len(self.game.record) - 1) // {'1': 2, '2': 4}[self.game_mode] + 1
                self.side = ' & '.join(map(lambda x: x.capitalize(), self.game.winner))
        except:
            ext = '.cns' if self.mode == 'save' else '.cnsr'
            print(f'ERROR loading saved file: {self.name}{ext}')
            self.err = True
        self.get_colors()

    def get_colors(self):
        # player mode color
        players = self.player_mode.split('v')
        if self.game_mode == '1':
            self.color[0] = [self.player_colors[i * 2 if players[i] == 'p' else 4] for i in range(2)]
        else:
            self.color[0] = [self.player_colors[i if players[i] == 'p' else 4] for i in range(4)]
        self.color[1] = self.side_colors.get(self.side, [self.color[2]] * 2)

    def in_range(self, b_pos, pos, *, align=(0, 0)):
        b_pos = utils.top_left(b_pos, self.size, align=align)
        return b_pos[0] < pos[0] < b_pos[0] + self.size[0] and b_pos[1] < pos[1] < b_pos[1] + self.size[1]

    def process_click(self, pos, mouse_pos, *, align=(0, 0)):
        pos = utils.top_left(pos, self.size, align=align)
        x0, x1, y0, y1, y2 = pos[0] + 650, pos[0] + 800, pos[1], pos[1] + self.size[1] // 2, pos[1] + self.size[1]
        if x0 < mouse_pos[0] < x1 and y0 < mouse_pos[1] < y1:
            return ['game', self.mode, self.player_mode, self.threshold, self.game]
        elif x0 < mouse_pos[0] < x1 and y1 < mouse_pos[1] < y2:
            return ['delete', self.mode, self.name]
        return [None]

    def show(self, ui, pos, *, align=(0, 0), pan=(0, 0)):
        pos = utils.top_left(pos, self.size, align=align)
        # SHOW BOX:
        # show background
        # show left
        if self.game_mode == '1':
            ui.show_div((pos[0], pos[1]), (200, self.size[1]), color=self.color[0][0], pan=pan)
            ui.show_div((pos[0] + 200, pos[1]), (400, self.size[1]), color=self.color[0][1], pan=pan)
        else:
            ui.show_div((pos[0], pos[1]), (200, self.size[1] // 2), color=self.color[0][0], pan=pan)
            ui.show_div((pos[0] + 200, pos[1]), (200, self.size[1] // 2), color=self.color[0][1], pan=pan)
            ui.show_div((pos[0], pos[1] + self.size[1] // 2), (200, self.size[1] // 2), color=self.color[0][3], pan=pan)
            ui.show_div((pos[0] + 200, pos[1] + self.size[1] // 2), (200, self.size[1] // 2), color=self.color[0][2],
                        pan=pan)
        # show middle
        ui.show_div((pos[0] + 400, pos[1]), (250, self.size[1] // 2), color=self.color[1][0], pan=pan)
        ui.show_div((pos[0] + 400, pos[1] + self.size[1] // 2), (250, self.size[1] // 2), color=self.color[1][1],
                    pan=pan)
        # show right
        ui.show_div((pos[0] + 650, pos[1]), (self.size[0] - 650, self.size[1]), color=self.color[2], pan=pan)
        # show border and lines
        ui.show_div(pos, self.size, border=2, pan=pan)
        ui.show_line((pos[0] + 400, pos[1]), (pos[0] + 400, pos[1] + self.size[1]), width=2, pan=pan)
        ui.show_line((pos[0] + 650, pos[1]), (pos[0] + 650, pos[1] + self.size[1]), width=2, pan=pan)
        ui.show_line((pos[0] + 650, pos[1] + self.size[1] // 2), (pos[0] + 800, pos[1] + self.size[1] // 2), width=2,
                     pan=pan)
        # SHOW NAME:
        ui.show_text((pos[0] + 50, pos[1] + self.size[1] // 2), self.name,
                     ('src', 'timesnewroman.ttf', 22), align=(0, 1), pan=pan)
        if not self.err:
            # SHOW GAME INFO:
            # show version
            ui.show_text((pos[0] + 450, pos[1] + self.size[1] // 2 - 36), f'Version {self.game_mode}',
                         ('src', 'timesnewroman.ttf', 18), align=(0, 1), pan=pan)
            # show player
            text = self.get_player_text()
            ui.show_text((pos[0] + 450, pos[1] + self.size[1] // 2 - 12), text,
                         ('src', 'timesnewroman.ttf', 18), align=(0, 1), pan=pan)
            # show round
            text = {
                'save': f'Round {self.round}',
                'replay': f'{self.round} round' if self.round == 1 else f'{self.round} rounds'
            }[self.mode]
            ui.show_text((pos[0] + 450, pos[1] + self.size[1] // 2 + 12), text,
                         ('src', 'timesnewroman.ttf', 18), align=(0, 1), pan=pan)
            # show current player or winner
            text = {
                'save': f'{self.side.capitalize()}\'s turn',
                'replay': f'{self.side} wins' if self.game_mode == '1' else f'{self.side} win'
            }[self.mode]
            ui.show_text((pos[0] + 450, pos[1] + self.size[1] // 2 + 36), text,
                         ('src', 'timesnewroman.ttf', 18), color=(0, 0, 0),
                         align=(0, 1), pan=pan)
        # show buttons
        ui.show_img((pos[0] + 725, pos[1] + self.size[1] // 4), 'play.png', align=(1, 1), pan=pan)
        ui.show_img((pos[0] + 725, pos[1] + 3 * self.size[1] // 4), 'delete.png', align=(1, 1), pan=pan)

    def get_player_text(self):
        return {
            'pvc': 'Single player (red)',
            'cvp': 'Single player (blue)',
            'pvp': 'Multiplayer (against)',
            'cvc': 'Bot game',
            'pvcvcvc': 'Single player (red)',
            'cvpvcvc': 'Single player (yellow)',
            'cvcvpvc': 'Single player (blue)',
            'cvcvcvp': 'Single player (green)',
            'pvpvcvc': 'Multiplayer (against)',
            'pvcvpvc': 'Multiplayer (against)',
            'pvcvcvp': 'Multiplayer (collaborate)',
            'cvpvpvc': 'Multiplayer (collaborate)',
            'cvpvcvp': 'Multiplayer (against)',
            'cvcvpvp': 'Multiplayer (against)',
            'pvpvpvc': 'Multiplayer (3 players)',
            'pvpvcvp': 'Multiplayer (3 players)',
            'pvcvpvp': 'Multiplayer (3 players)',
            'cvpvpvp': 'Multiplayer (3 players)',
            'cvcvcvc': 'Bot game',
        }[self.player_mode]
