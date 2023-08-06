#!/usr/bin/python

import click


@click.command()
@click.option('--data', required=True, type=(str))
def cli(data):
    if data:
        click.echo(data.upper())
    else:
        click.echo(data)

if __name__ == '__main__':
    cli()
