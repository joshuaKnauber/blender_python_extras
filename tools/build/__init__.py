import click
import json
import os
import inquirer
from colorama import Fore, Style
from .build import build_addon


@click.command(help="Creates a zipped version of the addon and cleans unused files and bpy tools.")
@click.option("--dirname", "-d", help="Name of the build directory", default="")
def build(dirname):
    dirname = get_dirname(dirname)
    print(f"{Fore.YELLOW}Building addon...{Style.RESET_ALL}")
    build_addon(dirname)
    print(f"{Fore.GREEN}Build complete{Style.RESET_ALL}")


def get_dirname(dirname):
    """ Gets the dirname from the build config or asks the user """
    config = {}
    with open(os.path.join(os.path.dirname(__file__), "build.config.json"), "r") as f:
        config = json.load(f)

    if not dirname:
        dirname = config["dirname"]

        if not dirname:
            dirname = inquirer.prompt([inquirer.Text('dirname', message="Name of the build directory", default="dist"),])["dirname"]

    with open(os.path.join(os.path.dirname(__file__), "build.config.json"), "w") as f:
        config["dirname"] = dirname
        json.dump(config, f, indent=4)
    
    return dirname