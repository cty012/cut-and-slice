import math
import random

import back.players.ai.nn as n
import back.players.ai.virtual_map as vm
import back.sprites.modules.map as m
import utils.functions as utils


class Minimax:
    def __init__(self, mode, map, side, friendly):
        self.mode = mode
        # map
        self.map = map
        self.size = len(self.map.board), len(self.map.board[0])
        # side
        self.all_sides = ['red', 'blue'] if self.mode == '1' else ['red', 'yellow', 'blue', 'green']
        self.side = side
        self.friendly = friendly
        # neural network
        self.nn = n.ValueNetwork(3 * self.size[0] * self.size[1], [108, 36])
        self.nn.load(f'{self.mode}.dict')

    def get_move(self):
        board = [[None for j in range(self.size[1])] for i in range(self.size[0])]
        m.MapLoader.save(self.map.board, board)
        node = Node(vm.VMap(self.mode, board, self.nn),
                    self.all_sides, self.side, self.friendly, [self.side] + self.friendly, depth=1)
        return node.get_best_move()


class Node:
    def __init__(self, vmap, all_sides, side, friendly, eval_sides, depth=1):
        # side
        self.all_sides = all_sides
        self.side = side
        self.friendly = friendly
        self.eval_sides = eval_sides
        # board
        self.vmap = vmap
        # moves and nodes
        self.depth = depth
        self.value = self.vmap.evaluate('', eval_sides)
        self.child_nodes = []
        # alpha beta prone
        self.alpha = -math.inf  # maximum value the node can choose
        self.beta = math.inf  # value the parent node would accept

    def get_child_nodes(self, moves, limit=None):
        n_side, n_friendly, n_opponents = utils.get_next(self.all_sides, self.side, self.friendly)
        self.child_nodes = [[
            Node(self.vmap.move(move[0], move[1]),
                 self.all_sides, n_side, n_friendly, self.eval_sides,
                 depth=self.depth - 1),
            move
        ] for move in moves]
        self.child_nodes.sort(key=lambda x: x[0].value, reverse=True)
        if limit is not None:
            self.child_nodes = self.child_nodes[:limit]

    def minimax_value(self):
        if self.depth <= 0:
            return self.value
        all_moves = self.vmap.get_all_moves(self.side)
        if len(all_moves) == 0:
            return self.value
        self.get_child_nodes(all_moves, limit=None)
        for node, move in self.child_nodes:
            value = node.minimax_value()
            self.alpha = max(self.alpha, value)
        return self.alpha

    def get_best_move(self):
        decision = ['next']
        all_moves = self.vmap.get_all_moves(self.side)
        if len(all_moves) == 0:
            return decision
        self.get_child_nodes(all_moves, limit=None)
        decisions = [None, None]
        dec_value = [self.alpha, self.alpha]
        for node, move in self.child_nodes:
            node_value = node.minimax_value()
            if dec_value[0] < node_value:
                decisions[0] = ['move'] + list(move)
                dec_value[0] = node_value
            elif dec_value[1] < node_value:
                decisions[1] = ['move'] + list(move)
                dec_value[1] = node_value
        # choose decision
        if decisions[1] is None:
            decision = decisions[0]
        else:
            prob = 0.5 + 0.5 * self.vmap.cover_rate()
            decision = decisions[0] if random.random() < prob else decisions[1]
        return decision
