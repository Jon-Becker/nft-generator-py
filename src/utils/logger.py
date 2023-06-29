import logging
import time


def get_logger(level: int) -> logging.Logger:
    logger = logging.getLogger("nft-generator-py")
    logger.setLevel(level)

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
