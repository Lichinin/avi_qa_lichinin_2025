import allure

from constants.constants import Constans


@allure.epic('Avito-intern test project')
@allure.suite('UI tests')
@allure.title('Тест поиска продукта')
def test_find_product(create_test_product, open_start_page):
    page = open_start_page
    page.find_product(Constans.CREATE_PRODUCT_NAME)
    page.assert_find_product()
