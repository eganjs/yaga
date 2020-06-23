__version__ = "0.1.0"

from pathlib import Path

import click


@click.group()
def cli():
    pass


@cli.command()
def targets():
    rules = []

    build_files = Path(".").glob("**/BUILD")
    for build_file in build_files:
        if build_file.exists():
            path = "/".join(build_file.parts[:-1])

            def genrule(name):  # noqa
                rules.append(f"//{path}:{name}")

            exec(build_file.read_text())

    for rule in rules:
        click.echo(rule)
