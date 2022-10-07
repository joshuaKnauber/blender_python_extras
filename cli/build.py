# all cli functionality for the build command goes in this file and commands are added to the cli in cli\cli.py

import click
import inquirer


@click.command()
def build():
    questions = [
        inquirer.Checkbox(
            'demo multi select',
            message="demo",
            choices=['one', 'two', 'three'],
        ),
    ]
    answers = inquirer.prompt(questions)
    print(answers)
    click.secho("Placeholder printing something in color", fg="green")
