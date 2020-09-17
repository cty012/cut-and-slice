import back.sprites.modules.map as m


class Log:
    def __init__(self, mode, player_mode, threshold):
        self.mode = mode
        self.player_mode = player_mode
        self.threshold = threshold
        self.record = []
        self.winner = []

    def push(self, command):
        self.record.append(command)

    def read(self):
        for command in self.record:
            yield command
