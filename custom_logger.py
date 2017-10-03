import logging
import sys

LOG_PATH = 'main.log'

def getLogger(log_name='', log_level=logging.DEBUG):
    if len(log_name.strip()) > 0:
        logger = logging.getLogger(log_name.strip())
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    else:
        logger = logging.getLogger()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    stdout_stream_handler = logging.StreamHandler(sys.stdout)
    stdout_stream_handler.setLevel(log_level)
    stdout_stream_handler.setFormatter(formatter)
    logger.addHandler(stdout_stream_handler)

    file_handler = logging.FileHandler(filename=LOG_PATH, mode='w')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.setLevel(log_level)
    return logger
