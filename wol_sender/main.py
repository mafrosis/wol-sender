import logging

import asyncio
from fastapi import APIRouter, FastAPI, Response
import uvicorn
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


fastapi.include_router(router)


def send(mac: str) -> bool:
    try:
        send_magic_packet(mac)
        logger.info('Waking %s', mac)
        return True

    except ValueError as e:
        logger.error(e)
        return False
