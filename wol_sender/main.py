import logging


logger = logging.getLogger('wol_sender')


def ohai(name: str):
    logger.info('Hello %s', name)
