import click
from tools import build



@click.group()
def cli():
    pass


cli.add_command(build.build)