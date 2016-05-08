import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logformat = '[%(levelname)s] %(name)s %(asctime)s : %(message)s'

handler = logging.StreamHandler()
formatter = logging.Formatter(logformat, datefmt = '%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)
