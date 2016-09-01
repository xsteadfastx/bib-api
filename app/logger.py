import logging

from logging.handlers import RotatingFileHandler


LOGGER = logging.getLogger('app')
LOGGER.setLevel(logging.DEBUG)

HANDLER = RotatingFileHandler(
    'bib-api.log',
    maxBytes=1024 * 1024 * 100,
    backupCount=20
)

formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s '
    '[in %(pathname)s:%(lineno)d]'
)

HANDLER.setFormatter(formatter)
HANDLER.setLevel(logging.DEBUG)

LOGGER.addHandler(HANDLER)
