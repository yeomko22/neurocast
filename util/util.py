import logging


def get_logger():
    logger = logging.getLogger("logger")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s', "%Y-%m-%d %H:%M:%S")
    stream_hander = logging.StreamHandler()
    stream_hander.setFormatter(formatter)
    logger.addHandler(stream_hander)
    return logger
