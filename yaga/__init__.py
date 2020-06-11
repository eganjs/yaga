__version__ = "0.1.0"

import click


@click.command()
@click.argument("name")
def main(name: str):
    print(f"Hello, {name}!")
