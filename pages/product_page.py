from locators.locators import Selectors
from pages.base_page import BasePage


class ProductPage(BasePage):

    def click_button_create(self):
        self.get_element(Selectors.CREATE_BUTTON).click()

    def assert_create_button_click(self):
        self.assert_equals(
            'Создать объявление',
            self.get_element(Selectors.CREATE_MODULE_TITLE).text.strip()
        )

    def assert_create_product(self):
        self.find_product(Selectors.CREATE_PRODUCT_NAME)
        self.assert_not_equals(
            'Найдено: 0',
            self.get_element(Selectors.SEARCH_RESULTS).text.strip()
        )

    def assert_find_product(self):
        self.assert_not_equals(
            'Найдено: 0',
            self.get_element(Selectors.SEARCH_RESULTS).text.strip()
        )
