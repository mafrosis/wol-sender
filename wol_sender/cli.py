import asyncio
import logging
import os

import click

from wol_sender.main import send as send_
from wol_sender.main import start as start_

logger = logging.getLogger('wol_sender')
sh = logging.StreamHandler()
logger.addHandler(sh)
logger.setLevel(logging.INFO)


@click.group()
@click.option('--debug', is_flag=True, default=False)
def cli(debug):
    # Set DEBUG logging based on ENV or --debug CLI flag
    if debug or os.environ.get('DEBUG'):
        logger.setLevel(logging.DEBUG)


@cli.command
@click.argument('mac')
def send(mac: str):
    send_(mac)


@cli.command
@click.option('--host', help='Bind server to hostname', default='127.0.0.1', type=str)
@click.option('--port', help='Bind server to port', default=3001, type=int)
def start(host: str, port: int):
    asyncio.run(start_(host, port))
