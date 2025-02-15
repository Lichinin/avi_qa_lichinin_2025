import allure

from api_client.api_client import ApiClient


@allure.epic('Avito-intern test project')
@allure.suite('API tests')
@allure.title('(TC_API_03) )олучить объявления по его идентификатору')
def test_getting_product(logger):
    api_client = ApiClient('https://qa-internship.avito.com', logger=logger)
    api_client.get_product_by_id(id='0cd4183f-a699-4486-83f8-b513dfde477a')
    api_client.assert_get_product_by_id_response()


@allure.epic('Avito-intern test project')
@allure.suite('API tests')
@allure.title('(TC_API_02) Получить статистику объявления по его id')
def test_getting_product_stat(logger):
    api_client = ApiClient('https://qa-internship.avito.com', logger=logger)
    api_client.get_product_stat(id='34553ac8-4b07-404c-8ea3-c284c24a59a9')
    api_client.assert_get_product_stat()


@allure.epic('Avito-intern test project')
@allure.suite('API tests')
@allure.title('(TC_API_01) Получить все объявления по id продавца')
def test_getting_products_by_seller_id(logger):
    api_client = ApiClient('https://qa-internship.avito.com', logger=logger)
    api_client.get_products_by_seller_id(id='12')
    api_client.assert_get_products_by_seller_id()


@allure.epic('Avito-intern test project')
@allure.suite('API tests')
@allure.title('(TC_API_04) Создание объявления')
def test_create_product(logger):
    api_client = ApiClient('https://qa-internship.avito.com', logger=logger)
    api_client.create_product(
        sellerid=737373,
        name='737373',
        price=737373
    )
    api_client.assert_create_product()
