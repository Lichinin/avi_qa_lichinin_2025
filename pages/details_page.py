import allure

from constants.constants import Constans
from locators.locators import Selectors
from pages.base_page import BasePage


class DetailsPage(BasePage):

    @allure.step('Клик по кнопке "Редактирование"')
    def click_button_edit(self):
        self.get_element(Selectors.EDIT_SAVE_BUTTON).click()

    @allure.step('Клик по кнопке сохранить изменения')
    def click_button_save_changes(self):
        self.get_element(Selectors.EDIT_SAVE_BUTTON).click()

    @allure.step('Проверка имени измененного продукта')
    def assert_edited_product_name(self):
        self.assert_equals(
            Constans.EDIT_PRODUCT_NAME,
            self.get_element(Selectors.DETAIL_PRODUCT_TITLE).text.strip()
        )

    @allure.step('Проверка цены измененного продукта')
    def assert_edited_product_price(self):
        self.assert_equals(
            Constans.EDIT_PRODUCT_PRICE,
            self.get_element(
                Selectors.DETAIL_PRODUCT_PRICE
                ).text.replace(' ', '').replace('₽', '')
        )

    @allure.step('Проверка описания измененного продукта')
    def assert_edited_product_description(self):
        self.assert_equals(
            Constans.EDIT_PRODUCT_DESCRIPTION,
            self.get_element(Selectors.DETAIL_PRODUCT_DESCRIPTION).text.strip()
        )

    @allure.step('Проверка изображения измененного продукта')
    def assert_edited_product_image(self):
        self.assert_equals(
            Constans.EDIT_PRODUCT_IMAGE,
            self.get_element(
                Selectors.DETAIL_PRODUCT_IMAGE
            ).get_attribute("src").split('/')[-1]
        )

    @allure.step('Проверка измененного продукта')
    def assert_edited_product(self):
        errors = []
        try:
            self.assert_edited_product_name
        except AssertionError as e:
            errors.append(f"Ошибка в проверке названия продукта: {e}")

        try:
            self.assert_edited_product_price
        except AssertionError as e:
            errors.append(f"Ошибка в проверке цены продукта: {e}")

        try:
            self.assert_edited_product_image
        except AssertionError as e:
            errors.append(f"Ошибка в проверке изображения продукта: {e}")

        try:
            self.assert_edited_product_description
        except AssertionError as e:
            errors.append(f"Ошибка в проверке описания продукта: {e}")

        if errors:
            raise AssertionError("\n".join(errors))
