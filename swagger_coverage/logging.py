import logging
import sys

l_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def setup(level: str):
    """
    Run logger
    :param level: logger level 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'
    """
    set_level = getattr(logging, level)
    formatter = logging.Formatter(l_format)
    logger = logging.getLogger()
    # Logger INFO
    info_handler = logging.StreamHandler(sys.stdout)
    info_handler.setLevel(set_level)
    info_handler.setFormatter(formatter)
    info_handler.addFilter(lambda rec: rec.levelno == set_level)
    logger.addHandler(info_handler)
    # Logger ERROR
    err_handler = logging.StreamHandler(sys.stderr)
    err_handler.setLevel(logging.ERROR)
    err_handler.setFormatter(formatter)
    err_handler.addFilter(lambda rec: rec.levelno == logging.ERROR)
    logger.addHandler(err_handler)
