from threading import Thread

import back.players.ai.minimax as m
import back.players.ai.opening as o
import utils.stopwatch as sw


class AIBot:
    def __init__(self, mode, map, log, side):
        self.mode = mode
        self.map = map
        self.log = log
        self.side = side
        self.friendly = []
        if self.mode == '2':
            self.friendly = {'red': ['green'], 'yellow': ['blue'], 'blue': ['yellow'], 'green': ['red']}[self.side]
        self.steps = 0
        # ai
        self.opening = o.Opening(self.mode, self.side)
        self.ai = m.Minimax(self.mode, self.map, self.side, self.friendly)
        self.stopwatch = sw.Stopwatch()
        self.speed = 1
        self.decision = None

    def process_click(self, pos, ctrl):
        ctrl.cursor = self.map.get_grid(pos)

    def get_move(self):
        if not self.stopwatch.is_running():
            self.stopwatch.clear()
            self.stopwatch.start()
            thread = Thread(target=self._get_move)
            thread.start()
        elif self.stopwatch.get_time() >= 1 and self.decision is not None:
            self.stopwatch.stop()
            decision, self.decision = self.decision, None
            if decision[0] == 'move':
                self.map.move(decision[1], decision[2])
                self.log.push(['move', decision[1], decision[2]])
                self.steps += 1
                return 'next'
            elif decision[0] == 'next':
                self.log.push(['next'])
                self.steps += 1
                return 'next'

    def _get_move(self):
        if self.mode == '1' and self.steps < 4 or self.mode == '2' and self.steps < 3:
            self.decision = self.opening.get_move()
        else:
            self.decision = self.ai.get_move()
        print(f'time: {self.stopwatch.get_time()}')
