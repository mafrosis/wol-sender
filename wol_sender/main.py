import asyncio
import logging
import subprocess

import uvicorn
from fastapi import APIRouter, FastAPI, Response
from wakeonlan import send_magic_packet

logger = logging.getLogger('wol_sender')

fastapi = FastAPI()
router = APIRouter()


async def start(host: str, port: int):
    'Start FastAPI'
    server = uvicorn.Server(config=uvicorn.Config(fastapi, loop='asyncio', host=host, port=port))

    await asyncio.wait([asyncio.create_task(server.serve())])


@router.get('/wake/{mac}', status_code=200)
async def wake(mac: str, response: Response):
    ret = send(mac)
    if not ret:
        response.status_code = 400

    return {'sent': ret, 'mac': mac}


@router.get('/check/{hostname}', status_code=200)
async def check(hostname: str, response: Response):
    ret = ping(hostname)
    if not ret:
        response.status_code = 400

    return {'ping': ret, 'hostname': hostname}


fastapi.include_router(router)


def send(mac: str) -> bool:
    'Broadcast WOL packet for MAC address'
    try:
        send_magic_packet(mac)
        logger.info('Waking %s', mac)
        return True

    except ValueError as e:
        logger.error(e)
        return False


def ping(hostname: str) -> bool:
    'Check if host is up via ping'
    if len(hostname.split('.')) != 4:
        # Function called with what appears to be a hostname and not an IP
        for line in subprocess.check_output(['nslookup', hostname, '192.168.1.1']).splitlines():
            if line.decode('utf8').startswith('Address: '):
                ip = line.decode('utf8').split(': ')[1]
                logger.info('Looked up %s for %s', ip, hostname)
                hostname = ip
                break

    logger.info('Sending ping to %s', hostname)
    return not bool(subprocess.call(['ping', '-c', '1', '-t', '1', hostname]))
