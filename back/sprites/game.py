import back.players.ai_bot as ai
import back.players.human as h
import back.sprites.log as l
import back.sprites.modules.controls as c
import back.sprites.modules.game_buttons as gb
import back.sprites.modules.game_menu as gm
import back.sprites.modules.map as m
import back.sprites.modules.score_board as sb


class Game:
    def __init__(self, args, mode, player_mode, threshold):
        self.args = args
        self.mode = mode
        self.player_mode = player_mode
        self.threshold = threshold
        self.name = ''
        # modules
        self.map = None
        self.log = None
        self.players = None
        self.ctrl = None
        self.game_menu = None
        self.game_buttons = None
        self.score_board = None

    def prepare(self):
        self.map = m.Map(self.mode, (self.args.size[0] // 2, self.args.size[1] // 2), align=(1, 1))
        self.log = l.Log(self.mode, self.player_mode, self.threshold)
        self.ctrl = c.Controls(self.map)
        self.game_menu = gm.GameMenu(self.mode, (self.args.size[0] - 15, 15), align=(2, 0))
        self.game_buttons = gb.GameButtons((self.args.size[0] - 15, self.args.size[1] - 15), self.log, align=(2, 2))
        self.score_board = sb.ScoreBoard(self.mode, self.map, self.threshold, (15, 15), align=(0, 0))
        self.set_players()

    def set_players(self):
        colors = self.game_menu.sides
        players = self.player_mode.split('v')
        self.players = [
            h.Human(self.map, self.log, colors[i]) if players[i] == 'p'
            else ai.AIBot(self.mode, self.map, self.log, colors[i])
            for i in range(len(players))
        ]

    def process_events(self, events):
        mouse_pos = events['mouse-pos']
        clicked = events['mouse-left'] == 'down'
        # game menu click events
        if clicked and self.game_menu.in_range(mouse_pos):
            return self.execute(self.game_menu.process_click(mouse_pos))
        # game button click events
        elif clicked and len(self.game_menu.winner) == 0 and \
                self.game_buttons.in_range(mouse_pos) and type(self.players[self.game_menu.current]) != ai.AIBot:
            self.execute(self.game_buttons.process_click(mouse_pos))
        # map click events
        elif clicked:
            self.execute(self.players[self.game_menu.current].process_click(mouse_pos, self.ctrl))
        # other events
        elif len(self.game_menu.winner) == 0:
            # map hover events
            self.ctrl.process_hover(mouse_pos)
            # player move
            self.execute(self.players[self.game_menu.current].get_move())

    def execute(self, name):
        if name == 'next':
            self.game_menu.winner = self.score_board.get_winner()
            if len(self.game_menu.winner) == 0:
                self.game_menu.next()
            elif len(self.log.winner) == 0:
                self.log.winner = self.game_menu.winner
        return name

    def move(self, units):
        pos = (self.map.pos[0] + units[0], self.map.pos[1] + units[1])
        pos = (min(pos[0], self.args.size[0] // 2), min(pos[1], self.args.size[1] // 2))
        size = self.map.total_size
        self.map.pos = [max(pos[0], self.args.size[0] // 2 - size[0]), max(pos[1], self.args.size[1] // 2 - size[1])]

    def show(self, ui):
        self.map.show(ui, cursor=self.ctrl.cursor, between=self.ctrl.between, side=self.game_menu.side())
        if len(self.game_menu.winner) == 0:
            self.game_buttons.show(ui)
        self.score_board.show(ui)
        self.game_menu.show(ui)
