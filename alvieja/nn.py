"""
__init__.py

Expample Neural Network
"""

import json
from os import path

import numpy as np
from numpy import around, array, dot

# inicializa el generador aleatorio de forma estatica
np.random.seed(1)  # pylint: disable=E1101


def sigmoid(x):  #pylint: disable=C0103
    """funcion Sigmoid, convierte un valor de -inf a +inf a uno de 0 a 1"""
    data = 1 / (1 + np.exp(-x))
    return around(data, 2)


def d_sigmoid_pos(x):  #pylint: disable=C0103
    """derivate of the sigmoid function"""
    return x * (1 - x)


def d_sigmoid_neg(x):  #pylint: disable=C0103
    """derivate of the sigmoid, inverted on x axis"""
    return 4 * (x - 0.5)**2


class SimpleNN:
    """Simplpe 1 layer Neural Net"""

    def __init__(self, name, inputs, hidden, outputs):
        self.name = name
        self.bias1 = 2 * np.random.random((1, hidden)) - 1
        self.bias2 = 2 * np.random.random((1, outputs)) - 1
        self.syn1 = 2 * np.random.random((inputs, hidden)) - 1
        self.syn2 = 2 * np.random.random((hidden, outputs)) - 1
        self.trainings = 0
        self.iterations = 0

    def __str__(self):
        return (
            "Neural Net {self.name} (trainings: "
            "{self.trainings}, iterations: {self.iterations})".format(
                **locals()))

    def save(self, folder):
        """Saves the synaptic data on a file"""
        filename = path.join(folder, '{self.name}.json'.format(**locals()))
        with open(filename, 'w') as _file:
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
        filename = path.join(folder, '{self.name}.json'.format(**locals()))
        if path.exists(filename):
            with open(filename, 'r') as _file:
                data = json.load(_file)
                self.iterations = data['iterations']
                self.trainings = data['trainings']
                syn1, syn2 = data['synapses']
                bias1, bias2 = data['bias']
                self.syn1, self.syn2 = array(syn1), array(syn2)
                self.bias1, self.bias2 = array(bias1), array(bias2)

    def _fordward_propagate(self, layer0):
        """Forward propagation"""
        layer1 = sigmoid(dot(layer0, self.syn1) + self.bias1)
        layer2 = sigmoid(dot(layer1, self.syn2) + self.bias2)
        return layer1, layer2

    def _backward_propagate(self, layer0, expected, progresive):
        """Backward propagation thourh the layers"""
        sign = 1 if progresive else -1
        # acelerator = d_sigmoid_pos if progresive else d_sigmoid_neg
        layer1, layer2 = self._fordward_propagate(layer0)
        l2_error = sign * (expected - layer2) * d_sigmoid_pos(layer2)
        l1_error = dot(l2_error, self.syn2.T) * d_sigmoid_pos(layer1)
        self.syn1 += dot(layer0.T, l1_error)
        l1_error_t = l1_error.T
        self.bias1 += [sum(l1_error_t[i]) for i in range(len(self.bias1))]
        self.syn2 += dot(layer1.T, l2_error)
        l2_error_t = l2_error.T
        self.bias2 += [sum(l2_error_t[i]) for i in range(len(self.bias2))]

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
