import utils.stopwatch as sw


class ReplayBot:
    def __init__(self, map, log):
        self.map = map
        self.log = log
        self.gen = self.log.read()
        self.stopwatch = sw.Stopwatch()
        self.speed = 1

    def process_click(self, pos, ctrl):
        ctrl.cursor = self.map.get_grid(pos)

    def get_move(self):
        if self.stopwatch.is_running() and self.stopwatch.get_time() >= 1:
            self.stopwatch.clear()
            self.stopwatch.start(self.speed)
            decision = next(self.gen, None)
            if decision[0] == 'move':
                self.map.move(decision[1], decision[2])
                return 'next'
            elif decision[0] == 'next':
                return 'next'
