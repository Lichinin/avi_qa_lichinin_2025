import allure

from api_client.api_client import ApiClient


@allure.epic('EM test project')
@allure.suite('API tests')
@allure.title('Получить объявления по его идентификатору')
def test_getting_repositories(logger):
    api_client = ApiClient('https://qa-internship.avito.com', product_id = '0cd4183f-a699-4486-83f8-b513dfde477a', logger = logger)
    api_client.get_product_by_id()
    api_client.asser_get_product_by_id_response()