"""game.py

The 3 in a row game itself
"""

from datetime import datetime
from pathlib import Path
from time import sleep

# class TicTacToeOld:
#     """Game of La Vieja(3 in a row)"""

#     P_1 = "P1"
#     P_2 = "P2"

#     def __init__(self):
#         self.board = None
#         self.reset()

#     def ended(self):
#         """Check if game have ended"""
#         return bool(not self.valid_moves() or self.winner())

#     def winner(self):
#         """Returns the wining player"""
#         for player in (self.P_1, self.P_2):
#             for i in range(3):
#                 if all((self.board[i][n] == player for n in range(3))):
#                     return player
#                 if all((self.board[n][i] == player for n in range(3))):
#                     return player
#             if all((self.board[i][i] == player for i in range(3))):
#                 return player
#             if all((self.board[i][2 - i] == player for i in range(3))):
#                 return player

#     def valid_moves(self):
#         """Return valid moves"""
#         # pylint: disable=C0103
#         moves = []
#         for x in range(3):
#             for y in range(3):
#                 if self.board[x][y] is None:
#                     moves.append((x, y))
#         return moves

#     def make_move(self, player, place):
#         """a player makes a move"""
#         # pylint: disable=C0103
#         assert player in (self.P_1, self.P_2), "player must be valid"
#         x, y = place
#         assert self.board[x][y] is None, "invalid move"
#         self.board[x][y] = player

#     def reset(self):
#         """resets the board"""
#         self.board = [[None for i in range(3)] for n in range(3)]


class TicTacToe:
    """Juego Normal"""

    def __init__(self, jugador1, jugador2, folder=None):
        for jugador in (jugador1, jugador2):
            assert hasattr(
                jugador, '__call__'), 'los jugadores deben ser ejecutables'
        self.jugadores = (jugador1, jugador2)
        self.folder = Path(folder) if folder else Path.cwd()
        self._tablero = [" "] * 9

    def partida_normal(self):
        """Una partida normal de la vieja"""
        self._tablero = [" "] * 9
        jugador = 0
        letra = lambda jug: 'o' if jug else 'x'
        print("Bienvenido al juego de la vieja")
        # inicar a los jugadores
        for jug in self.jugadores:
            jug.start()
            print(jug)
        turnos = 0
        # bucle del juego
        while True:
            turnos += 1
            jugador_actual = letra(jugador)
            jug = self.jugadores[jugador]
            sleep(1)  # para efecto cinematico
            # seleccion de jugador y calculo de jugada
            print('Tu turno {jug} ({jugador_actual})'.format(**locals()))
            pos = jug(self._tablero, jugador_actual, self.jugadas_validas)
            # actualizacion del tablero
            assert pos in self.jugadas_validas, 'esa jugada no es valida'
            self._tablero[pos] = jugador_actual
            self._dibujar_tablero()
            # Verificar fin del juego
            if self.gana(jugador_actual):
                if not jugador:  # x
                    self.jugadores[0].finish(1, turnos)
                    self.jugadores[1].finish(-1, turnos)
                else:  # o
                    self.jugadores[0].finish(-1, turnos)
                    self.jugadores[1].finish(1, turnos)
                print("Ha ganado las {jugador_actual}!".format(**locals()))
                break
            elif self.empate():
                for jug in self.jugadores:
                    jug.finish(0, turnos)
                print("Empate!")
                break
            jugador = 1 - jugador

    def juego_automatizado(self, partidas=1000, registrar=False):
        """Recrea n partidas entre los jugadores y mide las victorias"""
        assert (isinstance(partidas, int) and
                (partidas % 2) == 0), 'las partidas deben ser un numero par'
        registro, bitacoras = [], []
        for numero_partida in range(partidas):
            orden = (numero_partida % 2 == 0)
            ganador, bitacora = self._partida_automatica(orden)
            registro.append(ganador)
            bitacoras.append(bitacora)
        totales = self._calc_totales(registro)
        if registrar:
            self._guardar_bitacoras(bitacoras, totales)
        return totales

    @property
    def jugadas_validas(self):
        """Returns all valid moves"""
        return {i for i in range(9) if self._tablero[i] == ' '}

    def gana(self, jugador_actual):
        """Returns True if the current player wins, false otherwise"""
        tab, jug = self._tablero, jugador_actual
        check = lambda x, y, z: all([tab[i] == jug for i in (x, y, z)])
        pos = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7),
               (2, 5, 8), (0, 4, 8), (2, 4, 6))
        for _p in pos:
            if check(*_p):
                return True
        return False

    def empate(self):
        """Returns True if the game is a draw, false otherwise"""
        for i in self._tablero:
            if i == " ":
                return False
        return True

    def _dibujar_tablero(self):
        print(
            self._tablero[6] + "|" + self._tablero[7] + "|" +
            self._tablero[8])
        print('-----')
        print(
            self._tablero[3] + "|" + self._tablero[4] + "|" +
            self._tablero[5])
        print('-----')
        print(
            self._tablero[0] + "|" + self._tablero[1] + "|" +
            self._tablero[2])

    def _partida_automatica(self, orden=True):
        """Partida automatizada entre 2 ia"""
        bitacora = []
        self._tablero = [' '] * 9
        jugador = 0 if orden else 1
        letra = lambda jug: 'o' if jug else 'x'
        for jug in self.jugadores:
            jug.start()
        turnos = 0
        while True:
            turnos += 1
            jugador_actual = letra(jugador)
            try:
                pos = self.jugadores[jugador](
                    self._tablero, jugador_actual, self.jugadas_validas)
            except Exception as err:  #pylint: disable=W0703
                bitacora.append(err)
                return self.jugadores[1 - jugador], bitacora
            bitacora.append(pos)
            self._tablero[pos] = jugador_actual
            if self.gana(jugador_actual):
                self.jugadores[jugador].finish(1, turnos)
                self.jugadores[1 - jugador].finish(-1, turnos)
                return self.jugadores[jugador], bitacora
            elif self.empate():
                for jug in self.jugadores:
                    jug.finish(0, turnos)
                return None, bitacora
            jugador = 1 - jugador

    def _calc_totales(self, registro):
        jug1, jug2 = self.jugadores
        totales = {jug1: 0, jug2: 0, None: 0}
        for ganador in registro:
            totales[ganador] += 1
        return totales

    def _guardar_bitacoras(self, bitacoras, totales):
        jug1, jug2 = self.jugadores
        fecha = datetime.isoformat(datetime.today(), ' ')
        cabeza = '\n'.join((
            "Bitacora de competencia",
            "-" * 25,
            "fecha: {5}",
            "jugadores: 1-{0}, 2-{1}",
            "totales: {0}:  {2}, {1}:  {3}, empate: {4} ",
            "=" * 25,
        )).format(
            jug1, jug2, totales[jug1], totales[jug2], totales[None], fecha)
        lineas = []
        for _n, bitacora in enumerate(bitacoras):
            jugs = (str(jug1)[0], str(jug2)[0])[::1 if _n % 2 == 0 else -1]
            movs = []
            i = 0
            for mov in bitacora:
                movs.append('{0}->{1}'.format(jugs[i], mov))
                i = 1 - i
            lineas.append('%s) ' % _n + ' '.join(movs))
        _name = 'test_log_{}.txt'.format(fecha.split('.')[1])
        _filename = self.folder / _name
        with open(str(_filename), 'w') as _file:
            _file.write(cabeza + '\n' + '\n'.join(lineas))
