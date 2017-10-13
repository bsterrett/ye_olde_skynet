import json
from urllib.parse import urljoin

with open('secrets.json', 'r') as secrets_file_handle:
    secrets = json.load(secrets_file_handle)

BASE_URL = secrets['base_url']

class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver):
        self.driver = driver

    def go(self):
        url = urljoin(BASE_URL, self.url)
        self.driver.get(url)
