import logging
import logging.config


def setup_logging() -> None:
    logging.config.fileConfig('logging.conf')
