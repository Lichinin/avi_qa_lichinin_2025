import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from locators.locators import Selectors


class BasePage:

    def __init__(self, browser):
        self.browser = browser
        self.logger = browser.logger

    @allure.step('Поиск элемента на странице')
    def get_element(self, locator: tuple, timeout=3):
        with allure.step(f'Поиск эелемента "{locator}"'):
            try:
                self.browser.logger.info(f'* Get element "{repr(locator)}"')
                return WebDriverWait(self.browser, timeout).until(
                    EC.visibility_of_element_located(locator)
                )
            except Exception:
                allure.attach(
                    name="failure_screenshot",
                    body=self.browser.get_screenshot_as_png(),
                    attachment_type=allure.attachment_type.PNG
                )
            self.logger.exception('Error: element not found!')
            raise

    @allure.step('Проверка assert_equals')
    def assert_equals(self, expected, actual):
        self.logger.info('* Check assertion assert_equals')
        try:
            assert expected == actual, (
                f"Expected: '{expected}', Actual: '{actual}'"
            )
            self.logger.info('*** Test completed successful ***')
        except AssertionError:
            allure.attach(
                name="failure_screenshot",
                body=self.browser.get_screenshot_as_png(),
                attachment_type=allure.attachment_type.PNG
            )
            self.logger.exception('!!! Test failed !!!')
            raise

    @allure.step('Проверка assert_equals')
    def assert_not_equals(self, expected, actual):
        self.logger.info('* Check assertion assert_equals')
        try:
            assert expected != actual, (
                f"Expected: '{expected}', Actual: '{actual}'"
            )
            self.logger.info('*** Test completed successful ***')
        except AssertionError:
            allure.attach(
                name="failure_screenshot",
                body=self.browser.get_screenshot_as_png(),
                attachment_type=allure.attachment_type.PNG
            )
            self.logger.exception('!!! Test failed !!!')
            raise

    def paste_product_name(self, product_name):
        field = self.get_element(Selectors.PRODUCT_TITLE)
        field.clear()
        field.send_keys(product_name)

    def paste_product_price(self, product_price):
        field = self.get_element(Selectors.PRODUCT_PRICE)
        field.clear()
        field.send_keys(product_price)

    def paste_product_description(self, product_description):
        field = self.get_element(Selectors.PRODUCT_DESCRIPTION)
        field.clear()
        field.send_keys(product_description)

    def paste_product_image(self, product_image):
        field = self.get_element(Selectors.PRODUCT_IMAGE)
        field.clear()
        field.send_keys(product_image)

    def click_button_submit(self):
        self.get_element(Selectors.SUBMIT_BUTTON).click()

    def find_product(self, product_name):
        field = self.get_element(Selectors.SEARCH_FIELD)
        field.clear()
        field.send_keys(product_name)
        self.get_element(Selectors.SEARCH_BUTTON).click()

    def click_product_card(self):
        self.get_element(Selectors.PRODUCT_CARD).click()
