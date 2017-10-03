from selenium.webdriver.support.ui import WebDriverWait

class BasePageElement(object):
    """Base page class that is initialized on every page object class."""

    def __set__(self, obj, value):
    # def set_value(self, obj, owner):
        """Sets the text to the value supplied"""
        driver = obj.driver
        if self.locator[0] != 'css selector':
            raise 'Using a locator other than css'
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element_by_css_selector(self.locator[1]))
        driver.find_element_by_css_selector(self.locator[1]).send_keys(value)

    def __get__(self, obj, owner):
    # def get_value(self, obj, owner):
        """Gets the text of the specified object"""
        driver = obj.driver
        if self.locator[0] != 'css selector':
            raise 'Using a locator other than css'
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element_by_css_selector(self.locator[1]))
        element = driver.find_element_by_css_selector(self.locator[1])
        return element.get_attribute("value")
