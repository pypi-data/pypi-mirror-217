import json
import locale

import click

from xinv.config import get_default_config_path, get_sample_config, load_config
from xinv.renderer import render_invoice


@click.group()
def cli():
    pass


@cli.command()
def init():
    config_path = get_default_config_path()
    config = get_sample_config()

    with open(config_path, "w") as fp:
        fp.write(config.json(indent=4))

    click.echo(
        f"Initialized inv config at {config_path}.\n"
        "Edit it according to your needs and run `xinv create`."
    )


@cli.command()
@click.option("-o", "output_path", required=True, help="Output file path")
@click.option("--date-of-issue")
@click.option("--date-of-sale")
@click.option("--invoice-number")
def create(output_path: str, **kwargs):
    config_path = get_default_config_path()
    with open(config_path) as fp:
        config_data = json.load(fp)

    kwargs = {k: v for k, v in kwargs.items() if v}
    config_data.update(kwargs)
    config = load_config(config_data)

    render_invoice(config, output_path)


def main():
    locale.setlocale(locale.LC_ALL, "")

    cli()
