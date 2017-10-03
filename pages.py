from base_page import BasePage
from base_page_element import BasePageElement
from selenium.webdriver.common.by import By
import humanlike_pauses

class LoginPageLocators(object):
    USERNAME_TEXT = (By.CSS_SELECTOR, 'input[name="name"]')
    PASSWORD_TEXT = (By.CSS_SELECTOR, 'input[name="password"]')
    LOGIN_BUTTON = (By.CSS_SELECTOR, 'button#s1')

class GeneralUILocators(object):
    LINK_LIST_LINKS = (By.CSS_SELECTOR, 'div#sidebarBoxLinklist div.innerBox.content a')
    LOGOUT_LINK = (By.CSS_SELECTOR, 'a[href="logout.php"]')

class SendTroopsPageLocators(object):
    REINFORCEMENT_RADIO_BUTTON = (By.CSS_SELECTOR, 'input[value="2"]')
    NORMAL_ATTACK_RADIO_BUTTON = (By.CSS_SELECTOR, 'input[value="3"]')
    RAID_ATTACK_RADIO_BUTTON = (By.CSS_SELECTOR, 'input[value="4"]')
    SEND_RADIO_BUTTON = (By.CSS_SELECTOR, 'button#btn_ok')
    X_COORD_TEXT = (By.CSS_SELECTOR, 'input#xCoordInput')
    Y_COORD_TEXT = (By.CSS_SELECTOR, 'input#yCoordInput')

class LoginPage(BasePage):
    url = '/login.php'

    def authenticate(self, username, password):
        self.driver.find_element(*LoginPageLocators.USERNAME_TEXT).send_keys_slowly(username)
        humanlike_pauses.inter_field_delay()
        self.driver.find_element(*LoginPageLocators.PASSWORD_TEXT).send_keys_slowly(password)
        humanlike_pauses.inter_button_delay()
        self.driver.find_element(*LoginPageLocators.LOGIN_BUTTON).click()

class GeneralUIPage(BasePage):
    def get_farm_links(self):
        link_list_links = self.driver.find_elements(*GeneralUILocators.LINK_LIST_LINKS)
        return [link for link in link_list_links if 'Farm' in link.text]

class SendTroopsPage(BasePage):
    url = '/build.php?tt=2&id=39'

    def set_troop_allotment(self, troop_specifier, count):
        # input_element_locator = SendTroopsPageLocators.locator_for_troop_specifier(troop_specifier)
        input_element_locator = (By.CSS_SELECTOR, f"input[name=\"{troop_specifier}\"]")
        input_element = self.driver.find_element(*input_element_locator)
        input_element.send_keys_slowly(count)

    def set_action_type(self, action_type):
        formatted_action_type = action_type.strip().lower()
        if not formatted_action_type in ['reinforcement', 'normal', 'raid']:
            raise Exception(f"Unknown troop movement action type: {action_type}")

        if formatted_action_type == 'reinforcement':
            radio_button_element = self.driver.find_element(*SendTroopsPageLocators.REINFORCEMENT_RADIO_BUTTON)
        elif formatted_action_type == 'normal':
            radio_button_element = self.driver.find_element(*SendTroopsPageLocators.NORMAL_ATTACK_RADIO_BUTTON)
        elif formatted_action_type == 'raid':
            radio_button_element = self.driver.find_element(*SendTroopsPageLocators.RAID_ATTACK_RADIO_BUTTON)

        radio_button_element.click()

    def set_coordinates(self, x_coordinate, y_coordinate):
        self.driver.find_element(*SendTroopsPageLocators.X_COORD_TEXT).send_keys_slowly(x_coordinate)
        humanlike_pauses.inter_field_delay()
        self.driver.find_element(*SendTroopsPageLocators.Y_COORD_TEXT).send_keys_slowly(y_coordinate)

    def click_send_button(self):
        self.driver.find_element(*SendTroopsPageLocators.SEND_RADIO_BUTTON).click()

