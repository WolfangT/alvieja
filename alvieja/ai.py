"""artificial inteligences"""

from random import choice

from alvieja.nn import SimpleNN

POSICIONES = {
    "z": 0,
    "x": 1,
    "c": 2,
    "a": 3,
    "s": 4,
    "d": 5,
    "q": 6,
    "w": 7,
    "e": 8,
}


class Humano:
    """Objeto ejecutable para jugadas humanas"""

    ins_no_imp = True

    def __init__(self, nombre='Humano'):
        self.name = nombre

    def __str__(self):
        return self.name

    def start(self, *args):  #pylint: disable=W0613
        """Imprime las instruciones si no han sido impresas ya"""
        if Humano.ins_no_imp:
            print("Utiliza las letras z, x, c, a, s, d, q, w, e")
            print("para marcar tu posicion en el tablero como sigue")
            print("q|w|e")
            print("a|s|d")
            print("z|x|c")
            Humano.ins_no_imp = False

    def finish(self, resultado, turnos):
        """resultado"""
        pass

    def __call__(self, tablero, jugador_actual, valid_moves):  #pylint: disable=W0613
        while True:
            entrada = input()
            if entrada not in POSICIONES:
                print("Posicion invalida")
            else:
                pos = POSICIONES[entrada]
                if tablero[pos] == " ":
                    break
                else:
                    print("Posicion invalida")
        return pos


class IAEduardo:
    """Logaritmit IA from ed"""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Eduardo class bot <{self.name}>".format(**locals())

    def start(self, *args):  #pylint: disable=W0613
        """No me importa"""
        #pylint: disable=W0101
        return
        # print(f'{self.name}: u goin down')

    def finish(self, resultado, *args):  #pylint: disable=W0613
        """menos aun"""
        #pylint: disable=W0101
        return
        # if resultado == 1:
        #     print(
        #         f'{self.name}: >>> won tictactoe \n >>>'
        #         ' thinks its an acomplisment')
        # elif resultado == -1:
        #     print(f'{self.name}: sure why not')
        # else:
        #     print(f'{self.name}: yo no fui')

    def __call__(self, tablero, jugador_actual, valid_moves):  #pylint: disable=C0103
        """Eduardo IA"""
        #pylint: disable=C0103,C0330
        jugadas_validas = []
        jugadas_invalidas = []
        jugadores = []
        jugadores.append(jugador_actual)
        if jugadores[0] == "x":
            jugadores.append("o")
        if jugadores[0] == "o":
            jugadores.append("x")
        for j in range(2):
            for c in range(3):
                if c == 0:
                    if (((tablero[0] == jugadores[j]) +
                         (tablero[4] == jugadores[j]) +
                         (tablero[8] == jugadores[j])) == 2):
                        for p in range(0, 9, 4):
                            if tablero[p] == " ":
                                jugadas_validas.append(p)
                        if jugadas_validas != []:
                            pos = choice(jugadas_validas)
                            return pos
                    if (((tablero[2] == jugadores[j]) +
                         (tablero[4] == jugadores[j]) +
                         (tablero[6] == jugadores[j])) == 2):
                        for p in range(2, 7, 2):
                            if tablero[p] == " ":
                                jugadas_validas.append(p)
                        if jugadas_validas != []:
                            pos = choice(jugadas_validas)
                            return pos
                if (((tablero[c * 3] == jugadores[j]) +
                     (tablero[c * 3 + 1] == jugadores[j]) +
                     (tablero[c * 3 + 2] == jugadores[j])) == 2):
                    for p in range(c * 3, c * 3 + 3, 1):
                        if tablero[p] == " ":
                            jugadas_validas.append(p)
                    if jugadas_validas != []:
                        pos = choice(jugadas_validas)
                        return pos
                if (((tablero[c] == jugadores[j]) +
                     (tablero[c + 3] == jugadores[j]) +
                     (tablero[c + 6] == jugadores[j])) == 2):
                    for p in range(c, 9, 3):
                        if tablero[p] == " ":
                            jugadas_validas.append(p)
                    if jugadas_validas != []:
                        pos = choice(jugadas_validas)
                        return pos
        if tablero[4] == jugadores[1]:
            for i in range(0, 9, 2):
                if tablero[i] == " ":
                    jugadas_validas.append(i)
            if jugadas_validas != []:
                pos = choice(jugadas_validas)
                return pos
        if (tablero != [" ", " ", " ", " ", " ", " ", " ", " ", " "]
                and tablero[4] == " "):
            pos = 4
            return pos
        if 0 < (
            (tablero[1] == jugadores[1]) + (tablero[3] == jugadores[1]) +
            (tablero[5] == jugadores[1]) +
            (tablero[7] == jugadores[1])) < 4 or tablero[4] == jugadores[0]:
            if (((tablero[1] == jugadores[1]) + (tablero[3] == jugadores[1]) +
                 (tablero[5] == jugadores[1]) +
                 (tablero[7] == jugadores[1])) == 2):
                if (tablero[1] == jugadores[1] and tablero[5] == jugadores[1]
                        and tablero[2] == " "):
                    pos = 2
                    return pos
                if (tablero[1] == jugadores[1] and tablero[3] == jugadores[1]
                        and tablero[0] == " "):
                    pos = 0
                    return pos
                if (tablero[5] == jugadores[1] and tablero[7] == jugadores[1]
                        and tablero[8] == " "):
                    pos = 8
                    return pos
                if (tablero[7] == jugadores[1] and tablero[3] == jugadores[1]
                        and tablero[6] == " "):
                    pos = 6
                    return pos
            for i in range(1, 9, 2):
                if tablero[i] == " " and i != 4:
                    jugadas_validas.append(i)
            if (((tablero[1] != " ") + (tablero[4] != " ") +
                 (tablero[7] != " ")) == 2):
                for p in range(1, 9, 3):
                    if tablero[p] == " ":
                        jugadas_invalidas.append(p)
                jugadas_validas.remove(jugadas_invalidas[0])
                jugadas_invalidas.remove(jugadas_invalidas[0])
            if (((tablero[3] != " ") + (tablero[4] != " ") +
                 (tablero[5] != " ")) == 2):
                for p in range(3, 6, 1):
                    if tablero[p] == " ":
                        jugadas_invalidas.append(p)
                jugadas_validas.remove(jugadas_invalidas[0])
                jugadas_invalidas.remove(jugadas_invalidas[0])
            if jugadas_validas != []:
                pos = choice(jugadas_validas)
                return pos
        for i in range(0, 9, 2):
            if tablero[i] == " ":
                jugadas_validas.append(i)
        if jugadas_validas != []:
            pos = choice(jugadas_validas)
            return pos
        else:
            for i in range(9):
                if tablero[i] == " ":
                    jugadas_validas.append(i)
            if jugadas_validas != []:
                pos = choice(jugadas_validas)
        return pos


class IARandom:
    """IA player that chooses random valid moves
    """

    def __call__(self, tablero, jugador_actual, jugadas_validas):
        return choice(tuple(jugadas_validas))

    def __str__(self):
        return "Random Bot"

    def start(self):
        pass

    def finish(self, *args, **kwargs):
        pass


class IAWolfang:
    """Self learning 3 layer neural network"""

    def __init__(self, name='alvieja', neural_net=None):
        self.name = name
        self.neural_net = (
            neural_net if neural_net else SimpleNN(name, 18, 18, 9))
        self.name = name
        self.neural_net = neural_net
        self.match_moves = []
        self.invalid_moves = []
        self.vervose = False

    def start(self):
        """the game started"""
        self.match_moves = []
        self.invalid_moves = []

    def finish(self, result, turns):
        """the game ended"""
        fitness = 9 - turns
        repetitions = 5 * fitness**2 + 20
        inputs, outputs = zip(*self.match_moves)
        if result == 1:
            self.neural_net.train(inputs, outputs, True, 2 * repetitions)
        elif result == 0:
            self.neural_net.train(inputs, outputs, True, repetitions / 2)
        elif result == -1:
            self.neural_net.train(inputs, outputs, False, repetitions)

    def _transform_board(self, board, player):
        """Transform te board to be usable by the NN

        it returns a 18 element list, first 9 its the board
        with only player pieces as 1, last 9 it board with
        only oponent pieces as 1
        """
        processed = []
        for jug in True, False:
            for place in board:
                if place == " ":
                    processed.append(0)
                else:
                    processed.append(int((place == player) == jug))
        return processed

    def _get_ideal_ouput(self, move):
        return [0.75 if i == move else 0.25 for i in range(9)]

    # def __call__(self, board, player, valid_moves):
    #     inputs = self._transform_board(board, player)
    #     output = self.neural_net.calculate((inputs, ))
    #     moves = {i for i in range(9) if output[0][i] >= 0.9}
    #     posible_moves = moves.intersection(valid_moves)
    #     if not posible_moves:
    #         move = choice(tuple(valid_moves))
    #     else:
    #         move = sorted(posible_moves, key=lambda x: output[0][x])[0]
    #     if self.vervose:
    #         print('output: {output[0]}, selected: {move}'.format(**locals()))
    #     ideal_ouput = self._get_ideal_ouput(move)
    #     self.match_moves.append((inputs, ideal_ouput))
    #     return move

    def __call__(self, board, player, valid_moves):
        inputs = self._transform_board(board, player)
        output = self.neural_net.calculate((inputs, ))
        # moves = {i: output[0][i] for i in range(9) if output[0][i] > 0.5}
        moves = {i: output[0][i] for i in range(9)}
        ordered_moves = sorted(moves, key=lambda x: abs(0.75 - moves[x]))
        for move in ordered_moves:
            ideal_ouput = self._get_ideal_ouput(move)
            if move in valid_moves:
                self.match_moves.append((inputs, ideal_ouput))
                if self.vervose:
                    print(
                        'output: {output[0]}, selected: {move}'.format(
                            **locals()))
                return move
            else:
                self.invalid_moves.append((inputs, ideal_ouput))

    def __str__(self):
        return "Neural Network Player <{self.name}>".format(**locals())
