import allure

from constants.constants import Constans
from locators.locators import Selectors
from pages.base_page import BasePage


class ProductPage(BasePage):

    @allure.step('Клик по кнопке "Создать"')
    def click_button_create(self):
        self.get_element(Selectors.CREATE_BUTTON).click()

    @allure.step('Проверка клика по кнопке "Создать"')
    def assert_create_button_click(self):
        self.assert_equals(
            'Создать объявление',
            self.get_element(Selectors.CREATE_MODULE_TITLE).text.strip()
        )

    @allure.step('Проверет, что созданный продукт есть в базе')
    def assert_create_product(self):
        self.find_product(Constans.CREATE_PRODUCT_NAME)
        self.assert_not_equals(
            'Найдено: 0',
            self.get_element(Selectors.SEARCH_RESULTS).text.strip()
        )

    @allure.step('Проверка поиска продукта')
    def assert_find_product(self):
        self.assert_not_equals(
            'Найдено: 0',
            self.get_element(Selectors.SEARCH_RESULTS).text.strip()
        )
