"""test_nn.py

test the neural network
"""

from alvieja.nn import SimpleNN

# Datos de ejemplo
X = (
    (1, 1, 0),
    (1, 0, 1),
    (0, 1, 1),
    (0, 0, 1),
)
# Resultados de ejemplo
Y = (
    (1, ),
    (1, ),
    (0, ),
    (0, ),
)


def main():
    """Main process"""
    neural_net = SimpleNN('wolfang', 3, 5, 1)
    neural_net.load()
    # neural_net.train(X, Y)
    # neural_net.save()
    print(neural_net.calculate(X))
