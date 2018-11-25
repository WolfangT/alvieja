"""__main__.py

main module for the package
"""

from pathlib import Path

import click

from .ai import Humano, IAEduardo, IAWolfang, IARandom
from .game import TicTacToe
from .nn import SimpleNN, sgd, clr

# def start_gui():
#     """Starting point for the package"""
#     root = Tk()
#     Board(root)
#     root.mainloop()


class Conf:
    """Comand line interface for alvieja"""

    def __init__(self):
        self.folder = Path.cwd()
        self.name = 'alvieja'
        self.lr = None

    def get_players(self):
        """Loads the with AI with its saved progress"""
        print('#### Loading AI ####')
        if self.lr is None:
            self.lr = sgd(1000)
        neural_net = SimpleNN(self.name, 18, 10, 9)
        neural_net.load(self.folder)
        player1 = IAWolfang('Player 1', neural_net)
        player2 = IAWolfang('Player 2', neural_net)
        return player1, player2, neural_net

    def __str__(self):
        return "folder: {self.folder}, name: {self.name}".format(**locals())


pass_context = click.make_pass_decorator(Conf, ensure=True)


@click.group(chain=True)
@click.option(
    '-d',
    '--directory',
    type=click.Path(exists=True),
    help='Folder to store saves and reports')
@click.option(
    '-n',
    '--name',
    default='alvieja',
    help='Nane of the NN, determines its save file')
@click.option(
    "-l",
    '--learning-rate',
    type=click.Choice(['constant', 'a', 'b', 'c']),
    help='Set leaning rate',
    default='constant')
@pass_context
def cli(ctx, directory, name, learning_rate):
    """Auto learning neural network for playing la vieja"""
    click.echo('Wolcome to alvieja')
    click.echo(directory)
    ctx.name = name
    ctx.folder = Path(directory) if directory else Path.cwd()
    ctx.lr = {
        'constant': clr(0.01),
        'a': sgd(1000, 1),
        'b': sgd(1000, 2),
        'c': sgd(10000, 1),
    }[learning_rate]


@cli.command()
@click.argument('iterations', default=5000, type=int)
@click.argument('save_rate', default=500, type=int)
@click.option(
    "-O",
    '--oponent',
    type=click.Choice(['edbot', 'nn', 'random']),
    help='Set the oponent for the nn',
    default='nn')
@pass_context
def train(ctx, iterations, save_rate, oponent):
    """Trains the AI"""
    player1, player2, neural_net = ctx.get_players()
    if oponent == 'edbot':
        player2 = IAEduardo('edbot')
    elif oponent == 'random':
        player2 = IARandom()
    click.echo("playing {player1} against {player2}".format(**locals()))
    vieja_entrenamiento = TicTacToe(player1, player2, folder=ctx.folder)
    click.echo(("{neural_net} have "
                "played {neural_net.iterations} games").format(**locals()))
    click.echo('#### training {iterations} matches ####'.format(**locals()))
    for _i in range(iterations // save_rate):
        totals = vieja_entrenamiento.juego_automatizado(save_rate, False)
        click.echo(totals)
        neural_net.save(ctx.folder)
        click.echo(
            "played {save_rate} games, saving progress".format(**locals()))
    click.echo('#### training complete ####')


@cli.command()
@click.option(
    "-O",
    '--oponent',
    type=click.Choice(['edbot', 'nn', 'humano', 'random']),
    help='Set the oponent for the nn',
    default='edbot')
@pass_context
def test(ctx, oponent):
    """Tests the AI"""
    player1, player2, neural_net = ctx.get_players()
    click.echo("Starting testing for ia {neural_net}".format(**locals()))
    player2.vervose = True
    if oponent == 'edbot':
        click.echo('#### system test ####')
        vieja_prueba = TicTacToe(player1, IAEduardo('edbot'))
        click.echo(vieja_prueba.juego_automatizado(100))
        # print(
        #     f"{wolfbot} won {totals[wolfbot]},"
        #     f" lost {totals[edbot]}, "
        #     f"and draw {totals[None]} matches")
    elif oponent == "nn":
        click.echo('#### automated test ####')
        player1.vervose = True
        vieja_prueba = TicTacToe(player1, player2)
    elif oponent == 'humano':
        click.echo('#### Manual test ####')
        vieja_prueba = TicTacToe(Humano(), player2)
    elif oponent == 'random':
        click.echo('#### random test ####')
        vieja_prueba = TicTacToe(IARandom(), player2)
    vieja_prueba.partida_normal()


cli.add_command(train)
cli.add_command(test)

if __name__ == '__main__':
    cli()  #pylint: disable=E1120
