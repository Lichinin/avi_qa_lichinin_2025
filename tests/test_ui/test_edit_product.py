import allure

from constants.constants import Constans


@allure.epic('Avito-intern test project')
@allure.suite('UI tests')
@allure.title('Тест редактирования продукта')
def test_edit_product(create_test_product, open_product_details_page):
    page = open_product_details_page
    page.click_button_edit()
    page.paste_product_name(Constans.CREATE_PRODUCT_NAME)
    page.paste_product_price(Constans.CREATE_PRODUCT_PRICE)
    page.paste_product_description(Constans.CREATE_PRODUCT_DESCRIPTION)
    page.paste_product_image(Constans.CREATE_PRODUCT_IMAGE)
    page.click_button_save_changes()
    page.assert_new_product()
