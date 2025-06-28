import logging
import sys


def configure_logging(level=logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(level)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    ch.setFormatter(formatter)
    logger.addHandler(ch)
