from __future__ import division
from custom_logger import getLogger
from driver import pages, humanlike_pauses, action_queue
from os.path import isfile
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import numpy as np
import random
import re
import selenium

from IPython import embed

logger = getLogger('travian_driver')

REMOTE_SERVER_PORT = 4555
REMOTE_SERVER_URL = "http://localhost:{}/wd/hub".format(REMOTE_SERVER_PORT)

SESSION_ID_FILE_PATH = 'session_id.txt'

DEFAULT_WINDOW_SIZE = np.array([1280, 720], 'int')

class NoSessionIdFile(Exception): pass
class InsufficientTroopsError(Exception): pass

def session_id_file_exists():
    return isfile(SESSION_ID_FILE_PATH)

def get_session_id_from_file():
    if session_id_file_exists():
        with open(SESSION_ID_FILE_PATH, 'r') as file_handle:
            return file_handle.read().strip()
    else:
        raise NoSessionIdFile

def save_session_id_to_file(session_id):
    with open(SESSION_ID_FILE_PATH, 'w') as file_handle:
        file_handle.write(session_id)

class SessionRemote(webdriver.Remote):
    def start_session(self, desired_capabilities, browser_profile=None):
        # Skip the NEW_SESSION command issued by the original driver
        # and set only some required attributes
        self.w3c = True

def is_saved_session_valid(driver):
    try:
        random_resize(driver)
        return True
    except selenium.common.exceptions.WebDriverException as e:
        return False

def make_driver_from_saved_session():
    driver = SessionRemote(REMOTE_SERVER_URL, webdriver.DesiredCapabilities.FIREFOX)
    driver.session_id = get_session_id_from_file()
    return driver

def make_driver_with_new_session():
    driver = webdriver.Remote(REMOTE_SERVER_URL, webdriver.DesiredCapabilities.FIREFOX)
    save_session_id_to_file(driver.session_id)
    return driver

def get_driver():
    try:
        saved_session_driver = make_driver_from_saved_session()
        if is_saved_session_valid(saved_session_driver):
            logger.debug('Existing saved session is valid, re-attaching driver')
            return saved_session_driver
    except NoSessionIdFile:
        pass

    logger.debug('No valid saved session found, creating a new one and attaching driver')
    new_session_driver = make_driver_with_new_session()
    humanlike_pauses.brief_review_delay()
    return new_session_driver

def random_resize(driver):
    modified_size = DEFAULT_WINDOW_SIZE + np.random.randint(low=-20, high=20, size=2, dtype='int')
    driver.set_window_size(*modified_size)

class TravianDriver(selenium.webdriver.remote.webdriver.WebDriver):
    __wrapped_driver = None

    def __init__(self, travian_server_base_url):
        object.__setattr__(self, '_TravianDriver__wrapped_driver', get_driver())
        object.__setattr__(self, '_TravianDriver__travian_server_base_url', travian_server_base_url)

    def __getattr__(self, attr): # transparent proxy class
        return getattr(self.__wrapped_driver, attr)

    def __setattr__(self, attr, val): # transparent proxy class
        return setattr(self.__wrapped_driver, attr, val)

    def random_resize(self):
        random_resize(self)

    def select_own_village_by_name(self, name):
        own_village_links = self.__wrapped_driver.find_elements_by_css_selector('a[href^="?newdid="]')
        for village_link in own_village_links:
            village_name = village_link.text.split('\n')[0]
            if name.strip().upper() == village_name.strip().upper():
                logger.info(f"Changing active village to: {village_name!r}")
                village_link.click()
                return
        logger.error(f"Village name not found: {name!r}")

    def go_to_overview(self):
        pages.OverviewPage(self.__wrapped_driver).go()

    def go_to_capital_village_overview(self):
        self.select_own_village_by_name('Can Do!')
        self.go_to_overview()

    def log_in_test_strategies(self):
        def refresh():
            self.__wrapped_driver.refresh()
            self.__wrapped_driver.find_element(*pages.GeneralUILocators.LOGOUT_LINK)
        def check_reports():
            pages.ReportsPage(self.__wrapped_driver).go()
            self.__wrapped_driver.find_element(*pages.GeneralUILocators.LOGOUT_LINK)
        def check_overview():
            pages.OverviewPage(self.__wrapped_driver).go()
            self.__wrapped_driver.find_element(*pages.GeneralUILocators.LOGOUT_LINK)
        return [refresh, check_reports, check_overview]

    def random_log_in_test_strategy(self):
        test_stratetgy_functions = self.log_in_test_strategies()
        test_stratetgy_function = random.choice(test_stratetgy_functions)
        logger.debug(f"Using log in test strategy: {test_stratetgy_function.__name__}")
        return test_stratetgy_function

    def is_user_logged_in(self):
        try:
            self.random_log_in_test_strategy()()
            logger.debug('User is already logged in')
            return True
        except selenium.common.exceptions.NoSuchElementException:
            logger.debug('User is not logged in')
            return False

    def authenticate_if_necessary(self, username, password):
        if self.__wrapped_driver.current_url == 'about:blank':
            self.go_to_capital_village_overview()

        if not self.is_user_logged_in():
            pages.LoginPage(self.__wrapped_driver).authenticate(username, password)

    def send_troops(self, options):
        logger.info(f"Sending troops to {options['player']!r}")
        def _set_coordinates():
            send_troops_page.set_coordinates(options['x_coordinate'], options['y_coordinate'])

        def _set_troop_allotments():
            for troop_allotment in options['troop_allotments']:
                try:
                    available_troops_text = self.__wrapped_driver.find_element_by_css_selector(f"a[onclick^=\"document.snd.{troop_allotment['troop_specifier']}\"]").text
                except selenium.common.exceptions.NoSuchElementException:
                    message = f"Canceling movement, no troops of type {troop_allotment['troop_specifier']!r} available"
                    logger.warning(message)
                    raise InsufficientTroopsError(message)

                available_troops = int(available_troops_text)
                if available_troops >= troop_allotment['count']:
                    send_troops_page.set_troop_allotment(troop_allotment['troop_specifier'], troop_allotment['count'])
                else:
                    message = f"Canceling movement, insufficient troops of type {troop_allotment['troop_specifier']!r} ({available_troops} available, {troop_allotment['count']} required)"
                    logger.warning(message)
                    raise InsufficientTroopsError(message)

        def _set_action_type():
            send_troops_page.set_action_type(options['action_type'])

        form_action_queue = action_queue.ActionQueue([_set_coordinates, _set_troop_allotments, _set_action_type], insert_pause_action=humanlike_pauses.inter_field_delay)

        send_troops_page = pages.SendTroopsPage(self.__wrapped_driver)
        send_troops_page.go()

        humanlike_pauses.brief_review_delay()
        form_action_queue.run(ordered=False)
        send_troops_page.click_send_button() # click the send button on the allotment page

        humanlike_pauses.brief_review_delay() # TODO: more robust way to check that confirmation page has loaded
        send_troops_page.click_send_button() # click the send button on the confirmation page
        logger.info(f"Done sending troops to {options['player']!r}")

        humanlike_pauses.brief_review_delay()

    def get_villages_with_troop_movements(self):
        logger.debug('Getting list of villages with active troop movements')
        def get_villages_on_this_page():
            troop_movement_headlines = self.__wrapped_driver.find_elements_by_css_selector('td.troopHeadline > a')
            troop_movement_texts = [e.text for e in troop_movement_headlines]
            return_headlines = filter(lambda s: re.search(r'^Return from', s), troop_movement_texts)
            return_villages = map(lambda s: re.sub(r'^Return from (.*)', r"\1", s), return_headlines)
            raid_headlines = filter(lambda s: re.search(r'^Raid against', s), troop_movement_texts)
            raid_villages = map(lambda s: re.sub(r'^Raid against (.*)', r"\1", s), raid_headlines)
            return list(return_villages) + list(raid_villages)

        urls = [\
            'https://ts19.travian.us/build.php?gid=16&filter=1&tt=1&subfilters=2&page=1',
            'https://ts19.travian.us/build.php?gid=16&filter=2&tt=1&subfilters=4&page=1',
        ]
        all_villages = []
        for url in urls:
            self.__wrapped_driver.get(url)
            humanlike_pauses.brief_review_delay()
            try:
                pages = self.__wrapped_driver.find_element_by_css_selector('div.paginator').text.split(' ')
            except selenium.common.exceptions.NoSuchElementException:
                continue

            for page in pages:
                page_specific_url = url[:-1] + str(page)
                if self.__wrapped_driver.current_url != page_specific_url:
                    self.__wrapped_driver.get(page_specific_url)
                    humanlike_pauses.brief_review_delay()
                all_villages += get_villages_on_this_page()
        logger.debug('Done getting list of villages with active troop movements')
        return sorted(all_villages)

    def smart_raid(self, options_list):
        map_page = pages.MapPage(self.__wrapped_driver)
        overview_page = pages.OverviewPage(self.__wrapped_driver)

        # self.select_own_village_by_name('Sir Jams A Lot')
        self.select_own_village_by_name('Can Do!')
        exclusion_list = self.get_villages_with_troop_movements()
        filtered_options_list = [options for options in options_list if options['destination_village'] not in exclusion_list]

        out_of_troop_errors = 0
        out_of_troop_error_cutoff = 4
        for farm_options in filtered_options_list:
            try:
                self.send_troops(farm_options)
            except InsufficientTroopsError:
                out_of_troop_errors += 1
                if out_of_troop_errors >= out_of_troop_error_cutoff:
                    logger.warning(f"Canceling troop movements, {out_of_troop_error_cutoff} or more insufficient troop errors detected")
                    break
                overview_page.go()
                humanlike_pauses.stop_and_look_delay()
        logger.info('Done with sending troops')

        post_troop_movement_check = action_queue.ActionQueue(action_queue=[
            map_page.go,
            overview_page.go,
        ], insert_pause_action=humanlike_pauses.stop_and_look_delay)

        post_troop_movement_check.run(ordered=False)
