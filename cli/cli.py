import click

import init
import build


@click.group()
def cli():
    pass


cli.add_command(init.init)
cli.add_command(build.build)


if __name__ == '__main__':
    cli()