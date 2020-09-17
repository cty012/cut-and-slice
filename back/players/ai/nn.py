import os
import pickle


class ValueNetwork:
    def __init__(self, state_space, hidden_sizes):
        self.input_size = state_space
        self.output_size = 1
        self.hidden_sizes = hidden_sizes
        self.layers = []

    def load(self, filename):
        with open(os.path.join('.', 'src', 'model', filename), 'rb') as f:
            self.layers = pickle.load(f)

    def matsum(self, mat1, mat2):
        assert len(mat1) == len(mat2)
        assert len(mat1[0]) == len(mat2[0])
        i, j = len(mat1), len(mat1[0])
        return [[mat1[_i][_j] + mat2[_i][_j] for _j in range(j)] for _i in range(i)]

    def matmul(self, mat1, mat2):
        assert len(mat1[0]) == len(mat2)
        i, j, k = len(mat1), len(mat1[0]), len(mat2[0])
        return [[sum([mat1[_i][_j] * mat2[_j][_k] for _j in range(j)]) for _k in range(k)] for _i in range(i)]

    def relu(self, mat):
        return [[abs(mat[i][j]) for j in range(len(mat[0]))] for i in range(len(mat))]

    def forward(self, state):
        out1 = self.relu(self.matsum(self.matmul([state], self.layers[0]['weight']), [self.layers[0]['bias']]))
        out2 = self.relu(self.matsum(self.matmul(out1, self.layers[1]['weight']), [self.layers[1]['bias']]))
        out = self.matsum(self.matmul(out2, self.layers[2]['weight']), [self.layers[2]['bias']])
        return out[0][0]
