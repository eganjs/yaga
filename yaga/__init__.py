__version__ = "0.1.0"

from pathlib import Path

import click


@click.group()
def cli():
    pass


@cli.command()
def targets():
    rules = []

    build_file = Path("BUILD")
    if build_file.exists():

        def genrule(name):
            rules.append(name)

        exec(build_file.read_text())

    for rule in rules:
        click.echo(f"//:{rule}")
