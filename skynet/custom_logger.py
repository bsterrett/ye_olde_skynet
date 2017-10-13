import logging
import sys
from os.path import abspath

GLOBAL_LOG_PATH = abspath('logs/global.log')
DEFAULT_CUSTOM_LOG_PATH = abspath('logs/custom_logger.log')

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

    file_handler = logging.FileHandler(filename=GLOBAL_LOG_PATH, mode='w')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if len(log_name.strip()) == 0:
        custom_log_path = DEFAULT_CUSTOM_LOG_PATH
    else:
        custom_log_path = abspath(f"logs/{log_name}.log")
    file_handler = logging.FileHandler(filename=custom_log_path, mode='w')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.setLevel(log_level)
    return logger
