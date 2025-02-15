import json

import allure
import requests
from cerberus import Validator

from schemas.schemas import Schema


class ApiClient:
    def __init__(self, base_url, logger):
        self.base_url = base_url
        self.logger = logger

    @allure.step('Получение объявления по id')
    def get_product_by_id(self, id):
        url = self.base_url + f'/api/1/item/{id}'
        try:
            self.logger.info('* Try to get product by id')
            response = requests.get(url)
            response.raise_for_status()
            self.data = response.json()[0]
        except requests.exceptions.RequestException:
            self.logging.error(
                f'Failed get product by id'
                f'(status code = {response.status_code})'
            )
            raise Exception(
                f'Failed get product by id'
                f'(status code = {response.status_code})'
            )

    @allure.step('Проверка получения объявления по id')
    def assert_get_product_by_id_response(self):
        validator = Validator(Schema.product_details)
        self.logger.info('* Check response scheme')
        is_valid = validator.validate(self.data)
        if is_valid:
            self.logger.info('Response scheme valid')
        else:
            self.logger.error(
                f'Response scheme not valid: {validator.errors}'
            )
            raise AssertionError(
                f'Response scheme not valid: {validator.errors}'
            )
        self.logger.info(self.data)

    @allure.step('Получение статистики объявления по id')
    def get_product_stat(self, id):
        url = self.base_url + f'/api/1/statistic/{id}'
        try:
            self.logger.info('* Try to get stat by id')
            response = requests.get(url)
            response.raise_for_status()
            self.data = response.json()[0]
        except requests.exceptions.RequestException:
            self.logging.error(
                f'Failed get product by id'
                f'(status code = {response.status_code})'
            )
            raise Exception(
                f'Failed get product by id'
                f'(status code = {response.status_code})'
            )

    @allure.step('Проверка получения статистики по объявлению')
    def assert_get_product_stat(self):
        validator = Validator(Schema.product_stat)
        self.logger.info('* Check response scheme')
        is_valid = validator.validate(self.data)
        if is_valid:
            self.logger.info('Response scheme valid')
        else:
            self.logger.error(
                f'Response scheme not valid: {validator.errors}'
            )
            raise AssertionError(
                f'Response scheme not valid: {validator.errors}'
            )
        self.logger.info(self.data)

    @allure.step('Получение всех объявлений продавца по seller_id')
    def get_products_by_seller_id(self, id):
        url = self.base_url + f'/api/1/{id}/item'
        try:
            self.logger.info('* Try to get products by seller_id')
            response = requests.get(url)
            response.raise_for_status()
            self.data = response.json()
        except requests.exceptions.RequestException:
            self.logging.error(
                f'Failed get product by id'
                f'(status code = {response.status_code})'
            )
            raise Exception(
                f'Failed get product by id'
                f'(status code = {response.status_code})'
            )

    @allure.step('Проверка получения объявлений продавца по seller_id')
    def assert_get_products_by_seller_id(self):
        validator = Validator(Schema.product_details)
        self.logger.info('* Check response scheme')
        is_valid = [validator.validate(item) for item in self.data]
        if all(is_valid):
            self.logger.info('Response scheme valid')
        else:
            self.logger.error(f'Response scheme not valid: {validator.errors}')
            raise AssertionError(
                f'Response scheme not valid: {validator.errors}'
            )
        self.logger.info(self.data)

    @allure.step('Проверка создания объявления')
    def create_product(self, sellerid, name, price):
        url = self.base_url + '/api/1/item'
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "sellerID": sellerid,
            "name": name,
            "price": price,
        }
        try:
            self.logger.info('* Try to create product')
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(data)
            )
            response.raise_for_status()
            self.data = response.json()
        except requests.exceptions.RequestException:
            self.logging.error(
                f'Failed create product'
                f'(status code = {response.status_code})'
            )
            raise Exception(
                f'Failed create product'
                f'(status code = {response.status_code})'
            )

    @allure.step('Проверка ответа post-запроса')
    def assert_create_product(self):
        validator = Validator(Schema.create_product_response)
        self.logger.info('* Check response scheme')
        is_valid = validator.validate(self.data)
        if is_valid:
            self.logger.info('Response scheme valid')
        else:
            self.logger.error(f'Response scheme not valid: {validator.errors}')
            raise AssertionError(
                f'Response scheme not valid: {validator.errors}'
            )
        self.logger.info(self.data)
