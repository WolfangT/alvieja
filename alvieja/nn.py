"""
__init__.py

Expample Neural Network
"""

import json
import math
from pathlib import Path

import numpy as np
from numpy import array, dot

# inicializa el generador aleatorio de forma estatica
np.random.seed(1)  # pylint: disable=E1101


def sigmoid(x):  #pylint: disable=C0103
    """funcion Sigmoid, convierte un valor de -inf a +inf a uno de 0 a 1"""
    return 1 / (1 + np.exp(-x))


def d_sigmoid_pos(x):  #pylint: disable=C0103
    """derivate of the sigmoid function"""
    return x * (1 - x)


def d_sigmoid_neg(x):  #pylint: disable=C0103
    """derivate of the sigmoid, inverted on x axis"""
    return (x - 0.5)**2


def sgd(max_iterations):
    """Stochastic Gradient Descent with Warm Restarts,
    proposed by Loshchilov & Hutter

    :param max_iterations: number of iterations till the lr is resetted
    :type max_iterations: int
    """

    def learning_rate(iterations):
        return abs(math.cos(2 * iterations * math.pi / max_iterations))

    return learning_rate


class SimpleNN:
    """Simplpe 1 layer Neural Net"""

    def __init__(self, name, inputs, hidden, outputs):
        self.name = name
        self.bias1 = 2 * np.random.random((1, hidden)) - 1
        self.bias2 = 2 * np.random.random((1, outputs)) - 1
        self.syn1 = 2 * np.random.random((inputs, hidden)) - 1
        self.syn2 = 2 * np.random.random((hidden, outputs)) - 1
        self.learning_rate = sgd(100)
        self.trainings = 0
        self.iterations = 0

    def __str__(self):
        return (
            "Neural Net {self.name} (trainings: "
            "{self.trainings}, iterations: {self.iterations})".format(
                **locals()))

    def save(self, folder):
        """Saves the synaptic data on a file"""
        _name = '{self.name}.json'.format(**locals())
        filename = Path(folder) / _name
        with open(str(filename), 'w') as _file:
            json.dump(
                {
                    'trainings': self.trainings,
                    'iterations': self.iterations,
                    'synapses': (self.syn1.tolist(), self.syn2.tolist()),
                    'bias': (self.bias1.tolist(), self.bias2.tolist()),
                },
                _file,
                indent=4,
            )

    def load(self, folder):
        """Load the synaptic data from a file"""
        _name = '{self.name}.json'.format(**locals())
        filename = Path(folder) / _name
        if filename.exists():
            with open(str(filename), 'r') as _file:
                data = json.load(_file)
                self.iterations = data['iterations']
                self.trainings = data['trainings']
                syn1, syn2 = data['synapses']
                bias1, bias2 = data['bias']
                self.syn1, self.syn2 = array(syn1), array(syn2)
                self.bias1, self.bias2 = array(bias1), array(bias2)

    def _fordward_propagate(self, layer0):
        """Forward propagation"""
        layer1 = sigmoid(dot(layer0, self.syn1))  # + self.bias1)
        layer2 = sigmoid(dot(layer1, self.syn2))  # + self.bias2)
        return layer1, layer2

    def _backward_propagate(self, layer0, expected, progresive):
        """Backward propagation thourh the layers"""
        layer1, layer2 = self._fordward_propagate(layer0)
        learning_rate = self.learning_rate(self.iterations)
        dir_d_sigmoid = d_sigmoid_pos if progresive else d_sigmoid_neg
        error_size = (expected - layer2) if progresive else (0.5 - layer2)
        # dir_d_sigmoid = d_sigmoid_pos
        # error_size = (expected - layer2)
        l2_error = error_size * dir_d_sigmoid(layer2)
        l1_error = dot(l2_error, self.syn2.T) * dir_d_sigmoid(layer1)
        ajuste1 = dot(layer0.T, l1_error) * learning_rate
        ajuste2 = dot(layer1.T, l2_error) * learning_rate
        self.syn1 += ajuste1
        # self.bias1 += [sum(l1_error.T[i]) for i in range(len(self.bias1))]
        self.syn2 += ajuste2
        # self.bias2 += [sum(l2_error.T[i]) for i in range(len(self.bias2))]

    def calculate(self, inputs):
        """Calculates an answer to the imputs"""
        layer0 = array(inputs)
        return self._fordward_propagate(layer0)[1]

    def train(self, inputs, expected, progresive=True, times=1000):
        """Trains the NN on the input for an amount of times"""
        layer0 = array(inputs)
        for i in range(times):  #pylint: disable=W0612
            self._backward_propagate(layer0, array(expected), progresive)
        self.iterations += 1
        self.trainings += times
