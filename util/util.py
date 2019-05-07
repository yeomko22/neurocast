import logging
import json
import os


def get_logger():
    logger = logging.getLogger("")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s', "%Y-%m-%d %H:%M:%S")
    stream_hander = logging.StreamHandler()
    stream_hander.setFormatter(formatter)
    logger.addHandler(stream_hander)
    return logger

def readconfig():
    return json.loads(open(os.path.join(project_home(), 'config.json'), 'r').read())

def project_home():
    return os.getenv("BRAIN_FAC")

def data_home():
    return os.path.join(os.getenv("BRAIN_FAC"), 'data')

def checkpoint_home():
    return os.path.join(os.getenv("BRAIN_FAC"), 'data', 'checkpoint')
