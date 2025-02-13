import allure

from constants.constants import Constans


@allure.epic('Avito-intern test project')
@allure.suite('UI tests')
@allure.title('Тест нажатия кнопки "Создать"')
def test_button_create(open_start_page):
    page = open_start_page
    page.click_button_create()
    page.assert_create_button_click()


@allure.epic('Avito-intern test project')
@allure.suite('UI tests')
@allure.title('Тест создания нового продукта')
def test_create_product(open_start_page):
    page = open_start_page
    page.click_button_create()
    page.paste_product_name(Constans.CREATE_PRODUCT_NAME)
    page.paste_product_price(Constans.CREATE_PRODUCT_PRICE)
    page.paste_product_description(Constans.CREATE_PRODUCT_DESCRIPTION)
    page.paste_product_image(Constans.CREATE_PRODUCT_DESCRIPTION)
    page.click_button_submit()
    page.find_product(Constans.CREATE_PRODUCT_NAME)
    page.assert_create_product()
