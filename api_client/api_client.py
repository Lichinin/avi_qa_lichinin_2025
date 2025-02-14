import json
import os
from cerberus import Validator

import allure
import requests


class ApiClient:
    def __init__(self, base_url, product_id, logger):
        self.base_url = base_url
        self.product_id = product_id
        self.logger = logger


    @allure.step('Получения объявления по id')
    def get_product_by_id(self):
        url = self.base_url + f'/api/1/item/{self.product_id}'
        try:
            self.logger.info('* Try to get user repositories"')
            response = requests.get(url)
            response.raise_for_status()
            a = response.json()
            b = response[0]
            data = response.json()
            self.data = b
        except requests.exceptions.RequestException:
            self.logging.error(f"Ошибка получения объявления (status code = {response.status_code})")
            raise Exception(f"Ошибка получения объявления (status code = {response.status_code})")

    def asser_get_product_by_id_response(self):
        schema = {
            "id": {"type": "string", "required": True},
            "sellerId": {"type": "string", "required": True},
            "name": {"type": "string", "required": True},
            "price": {"type": "integer", "required": True},
            "createdAt": {"type": "string", "required": True},
            "statistics": {
                "type": "dict",
                "nullable": True,
                "required": True,
                "schema": {
                    "likes": {"type": "integer", "required": True},
                    "viewCount": {"type": "integer", "required": True},
                    "contacts": {"type": "integer", "required": True},
                },
            },
        }
        validator = Validator(schema)
        is_valid = validator.validate(json.loads(self.data))
        if is_valid:
            self.logger.info("Valid!")
        else:
            self.logger.info("Not valid:", validator.errors)
        self.logger.info(self.data)