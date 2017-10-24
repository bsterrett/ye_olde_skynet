from IPython import embed
from custom_logger import getLogger
from driver import travian_driver, pages, humanlike_pauses, action_queue
from driver.selenium_server_utils import launch_selenium_standalone_server_if_necessary
from time import sleep
import json
import random

logger = getLogger('main')

with open('secrets.json', 'r') as secrets_file_handle:
    secrets = json.load(secrets_file_handle)

def execute():
    launch_selenium_standalone_server_if_necessary()
    driver = travian_driver.TravianDriver(secrets['base_url'])
    reports_page = pages.ReportsPage(driver)
    messages_page = pages.MessagesPage(driver)
    overview_page = pages.OverviewPage(driver)

    driver.authenticate_if_necessary(secrets['username'], secrets['password'])

    post_login_check = action_queue.ActionQueue(action_queue=[
        messages_page.go,
        reports_page.go,
        overview_page.go,
    ], insert_pause_action=humanlike_pauses.stop_and_look_delay)
    post_login_check.run(ordered=False)
    humanlike_pauses.stop_and_look_delay()

    # with open('data/farm_options_list_portia.json', 'r') as farm_options_file_handle:
    with open('data/farm_options_list.json', 'r') as farm_options_file_handle:
        farm_options_list = json.load(farm_options_file_handle)
    random.shuffle(farm_options_list)

    driver.smart_raid(farm_options_list)


if __name__ == '__main__':
    logger.debug('Beginning main loop')
    execute()
    logger.debug('Done with main loop')
