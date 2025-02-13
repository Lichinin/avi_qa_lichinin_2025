import allure

from locators.locators import Selectors
from pages.base_page import BasePage


class DetailsPage(BasePage):

    @allure.step('Клик по кнопке "Редактирование"')
    def click_button_edit(self):
        self.get_element(Selectors.EDIT_SAVE_BUTTON).click()

    @allure.step('Клик по кнопке сохранить изменения')
    def click_button_save_changes(self):
        self.get_element(Selectors.EDIT_SAVE_BUTTON).click()

    @allure.step('Проверка имени созданного продукта')
    def assert_new_product_name(self):
        self.assert_equals(
            Selectors.NEW_PRODUCT_NAME,
            self.get_element(Selectors.DETAIL_PRODUCT_TITLE).text.strip()
        )

    @allure.step('Проверка цены созданного продукта')
    def assert_new_product_price(self):
        self.assert_equals(
            Selectors.NEW_PRODUCT_PRICE,
            self.get_element(
                Selectors.DETAIL_PRODUCT_PRICE
                ).text.replace(' ', '').replace('₽', '')
        )

    @allure.step('Проверка описания созданного продукта')
    def assert_new_product_description(self):
        self.assert_equals(
            Selectors.NEW_PRODUCT_DESCRIPTION,
            self.get_element(Selectors.DETAIL_PRODUCT_DESCRIPTION).text.strip()
        )

    @allure.step('Проверка изображения созданного продукта')
    def assert_new_product_image(self):
        self.assert_equals(
            Selectors.NEW_PRODUCT_IMAGE,
            self.get_element(
                Selectors.DETAIL_PRODUCT_IMAGE
            ).get_attribute("src").split('/')[-1]
        )

    @allure.step('Проверка созданного продукта')
    def assert_new_product(self):
        errors = []
        try:
            self.assert_equals(
                Selectors.NEW_PRODUCT_NAME,
                self.get_element(Selectors.DETAIL_PRODUCT_TITLE).text.strip()
            )
        except AssertionError as e:
            errors.append(f"Ошибка в проверке названия продукта: {e}")

        try:
            self.assert_equals(
                Selectors.NEW_PRODUCT_PRICE,
                self.get_element(
                    Selectors.DETAIL_PRODUCT_PRICE
                ).text.replace(' ', '').replace('₽', '')
            )
        except AssertionError as e:
            errors.append(f"Ошибка в проверке цены продукта: {e}")

        try:
            self.assert_equals(
                Selectors.NEW_PRODUCT_IMAGE,
                self.get_element(
                    Selectors.DETAIL_PRODUCT_IMAGE
                ).get_attribute("src").split('/')[-1]
            )
        except AssertionError as e:
            errors.append(f"Ошибка в проверке изображения продукта: {e}")

        try:
            self.assert_equals(
                Selectors.NEW_PRODUCT_DESCRIPTION,
                self.get_element(
                    Selectors.DETAIL_PRODUCT_DESCRIPTION
                ).text.strip()
            )
        except AssertionError as e:
            errors.append(f"Ошибка в проверке описания продукта: {e}")

        if errors:
            raise AssertionError("\n".join(errors))
