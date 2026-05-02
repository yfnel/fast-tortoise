import logging

logger = logging.getLogger(__name__)

def run() -> None:
    logger.debug('hello from %s', __name__)
