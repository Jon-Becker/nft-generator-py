import logging
import time
from typing import Any

from alive_progress import alive_bar


def get_logger(level: int) -> logging.Logger:
    logger = logging.getLogger("nft-generator-py")
    logger.setLevel(logging.DEBUG if level > 0 else logging.INFO)

    # create formatter
    logging.Formatter.converter = time.gmtime
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # set to debug
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    logger.propagate = False
    return logger


def get_progress_bar(total: int) -> Any:
    prefix = ("[{}]: ").format(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
    return alive_bar(
        total,
        title=prefix,
        enrich_print=False,
        receipt=False,
        spinner=False,
        stats="(eta: {eta})",
    )
