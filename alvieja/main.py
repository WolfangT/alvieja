"""__main__.py

main module for the package
"""

from pathlib import Path

import click

from alvieja.ai import Humano, IAEduardo, IAWolfang
from alvieja.game import TicTacToe
from alvieja.nn import SimpleNN

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

    def get_players(self):
        """Loads the with AI with its saved progress"""
        print('#### Loading AI ####')
        neural_net = SimpleNN(self.name, 18, 18, 9)
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
@pass_context
def cli(ctx, directory, name):
    """Auto learning neural network for playing la vieja"""
    click.echo('Wolcome to alvieja')
    click.echo(directory)
    ctx.name = name
    ctx.folder = Path(directory) if directory else Path.cwd()


@cli.command()
@click.argument('iterations', default=5000, type=int)
@click.argument('save_rate', default=500, type=int)
@pass_context
def train(ctx, iterations, save_rate):
    """Trains the AI"""
    player1, player2, neural_net = ctx.get_players()
    vieja_entrenamiento = TicTacToe(player1, player2, folder=ctx.folder)
    click.echo(("{neural_net} have "
                "played {neural_net.iterations} games").format(**locals()))
    click.echo('#### training {iterations} matches ####'.format(**locals()))
    for _i in range(iterations // save_rate):
        vieja_entrenamiento.juego_automatizado(save_rate, False)
        neural_net.save(ctx.folder)
    vieja_entrenamiento.juego_automatizado(iterations % save_rate)
    neural_net.save(ctx.folder)


@cli.command()
@click.option(
    '--automatic/--manual',
    default=True,
    help='Set to manual to play against the NN')
@pass_context
def test(ctx, automatic):
    """Tests the AI"""
    player1, player2, neural_net = ctx.get_players()
    click.echo("Starting testing for ia {neural_net}".format(**locals()))
    if automatic:
        click.echo('#### automated test ####')
        edbot = IAEduardo('edbot')
        vieja_prueba = TicTacToe(edbot, player1, folder=ctx.folder)
        totals = vieja_prueba.juego_automatizado(10, True)
        # print(
        #     f"{wolfbot} won {totals[wolfbot]},"
        #     f" lost {totals[edbot]}, "
        #     f"and draw {totals[None]} matches")
        click.echo(totals)
    else:
        click.echo('#### Manual test ####')
        vieja_prueba_humano = TicTacToe(Humano('wolfang'), player2)
        vieja_prueba_humano.partida_normal()


cli.add_command(train)
cli.add_command(test)

if __name__ == '__main__':
    cli()  #pylint: disable=E1120
