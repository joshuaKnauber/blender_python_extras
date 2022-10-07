import click


@click.command(help="Initializes bpy tools for this addon")
@click.argument("name", required=False)
def init(name):
    print("Got name", name)