import numpy as np


class Softmax:
    def __init__(self, input_len, nodes):
        """
        Initializes softmax layer

        Parameters:
            input_len:
                Length of input from previous layer
            nodes:
                Nodes from previous layer


        """
        self.weights = np.random.randn(input_len, nodes) / input_len
        self.biases = np.zeros(nodes)

    def forward(self, input):
        """
        Forward pass of softmax layer.

        Parameters:
            input:
                Any array with any dimensions (It will be flattened)

        Returns:
            1D numpy array containing respective probabilities
        """
        input = input.flatten()

        input_len, nodes = self.weights.shape
        totals = np.dot(input, self.weights) + self.biases
        exp = np.exp(totals)
        return exp / np.sum(exp, axis=0)
