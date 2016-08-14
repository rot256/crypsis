import logging
from random import SystemRandom
from logging import DEBUG, INFO, WARNING, ERROR

### Setup shared logging ###

logger = logging.getLogger(__name__)

def log_level(level):
    logger.setLevel(level)

logger.setLevel(logging.INFO)

logformat = '[%(levelname)s] %(name)s %(asctime)s : %(message)s'

handler = logging.StreamHandler()
formatter = logging.Formatter(logformat, datefmt = '%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)

### Setup shared CSPRNG ###

csprng = SystemRandom()
