import allure

from constants.constants import Constans


@allure.epic('Avito-intern test project')
@allure.suite('UI tests')
@allure.title('(TC_UI_02) Тест редактирования продукта')
def test_edited_product(create_test_product, open_product_details_page):
    page = open_product_details_page
    page.click_button_edit()
    page.paste_product_name(Constans.EDIT_PRODUCT_PRICE)
    page.paste_product_price(Constans.EDIT_PRODUCT_PRICE)
    page.paste_product_description(Constans.EDIT_PRODUCT_DESCRIPTION)
    page.paste_product_image(Constans.EDIT_PRODUCT_IMAGE)
    page.click_button_save_changes()
    page.assert_edited_product()
