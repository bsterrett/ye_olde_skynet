import selenium

from driver import humanlike_pauses
from selenium.webdriver.common.utils import keys_to_typing

def send_keys_slowly(self, *value):
    value_as_keys = keys_to_typing(value)
    for v in value_as_keys[:-1]:
        self.send_keys(v)
        humanlike_pauses.inter_key_delay()
    self.send_keys(value_as_keys[-1])

selenium.webdriver.remote.webelement.WebElement.send_keys_slowly = send_keys_slowly
