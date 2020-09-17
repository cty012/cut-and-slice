import random

import back.players.ai.virtual_map as vm
import back.sprites.modules.map as m


class RandomMove:
    def __init__(self, map, side):
        self.map = map
        self.size = len(self.map.board), len(self.map.board[0])
        self.side = side

    def get_move(self):
        board = [[None for j in range(self.size[1])] for i in range(self.size[0])]
        m.MapLoader.save(self.map.board, board)
        vmap = vm.VMap(board)
        all_moves = vmap.get_all_moves(self.side)
        if len(all_moves) > 0:
            move = random.choice(all_moves)
            return ['move', move[0], move[1]]
        else:
            return ['next']
