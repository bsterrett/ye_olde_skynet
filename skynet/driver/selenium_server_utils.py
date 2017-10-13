from custom_logger import getLogger
from os.path import abspath
from subprocess import Popen
from time import sleep

JAVA_PATH = '/usr/bin/java'
SHELL_PATH = '/bin/bash'
LAUNCH_SERVER_STANDALONE_SCRIPT_PATH = abspath('bin/launch_selenium_server_standalone.sh')
RUNNING_SERVER_TEST_SCRIPT_PATH = abspath('bin/running_selenium_server_test.sh')

LAUNCH_STANDALONE_SERVER_ARGS = [
    SHELL_PATH,
    LAUNCH_SERVER_STANDALONE_SCRIPT_PATH
]

RUNNING_STANDALONE_SERVER_TEST_ARGS = [
    SHELL_PATH,
    RUNNING_SERVER_TEST_SCRIPT_PATH
]

logger = getLogger('standalone_server_utils')

def launch_selenium_standalone_server():
    logger.info('Launching a new selenium standalone server as a daemon')
    p = Popen(LAUNCH_STANDALONE_SERVER_ARGS)
    logger.info('Waiting for server to initialize')
    sleep(15)
    logger.info(f"New selenium standalone server successfully started, pid: {p.pid}")

def is_selenium_standalone_server_running():
    p = Popen(RUNNING_STANDALONE_SERVER_TEST_ARGS)
    p.communicate()
    if p.returncode == 0:
        logger.info('Detected running selenium standalone server')
        return True
    else:
        logger.info('No running selenium standalone server found')
        return False

def launch_selenium_standalone_server_if_necessary():
    if not is_selenium_standalone_server_running():
        launch_selenium_standalone_server()

if __name__ == '__main__':
    launch_selenium_standalone_server_if_necessary()
