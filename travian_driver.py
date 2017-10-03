from __future__ import division
from custom_logger import getLogger
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import numpy as np
import os
import pages
import selenium
import urllib.parse
import humanlike_pauses

logger = getLogger('travian_driver')

REMOTE_SERVER_PORT = 4555
REMOTE_SERVER_URL = "http://localhost:{}/wd/hub".format(REMOTE_SERVER_PORT)

SESSION_ID_FILE_PATH = 'session_id.txt'

DEFAULT_WINDOW_SIZE = np.array([1280, 720], 'int')

class NoSessionIdFile(Exception): pass

def session_id_file_exists():
    return os.path.isfile(SESSION_ID_FILE_PATH)

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
            logger.debug('USING SAVED SESSION DRIVER')
            return saved_session_driver
    except NoSessionIdFile:
        pass

    logger.debug('USING NEW SESSION DRIVER')
    new_session_driver = make_driver_with_new_session()
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

    def go_to_capital_village_overview(self):
        url = urllib.parse.urljoin(self.__travian_server_base_url, 'dorf1.php')
        self.get(url)

    def is_user_logged_in(self):
        try:
            self.__wrapped_driver.refresh()
            self.__wrapped_driver.find_element(*pages.GeneralUILocators.LOGOUT_LINK)
            return True
        except selenium.common.exceptions.NoSuchElementException:
            return False

    def send_troops(self, options):
        send_troops_page = pages.SendTroopsPage(self.__wrapped_driver)
        send_troops_page.go()

        humanlike_pauses.brief_review_delay()
        send_troops_page.set_coordinates(options['x_coordinate'], options['y_coordinate'])
        humanlike_pauses.inter_field_delay()
        for troop_allotment in options['troop_allotments']:
            send_troops_page.set_troop_allotment(troop_allotment['troop_specifier'], troop_allotment['count'])
        humanlike_pauses.inter_button_delay()
        send_troops_page.set_action_type(options['action_type'])
        humanlike_pauses.brief_review_delay()
        send_troops_page.click_send_button() # click the send button on the allotment page

        humanlike_pauses.brief_review_delay() # TODO: more robust way to check that confirmation page has loaded
        send_troops_page.click_send_button() # click the send button on the confirmation page
        humanlike_pauses.brief_review_delay()

