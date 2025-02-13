from selenium.webdriver.common.by import By

from constants.constants import Constans


class Selectors:

    CREATE_BUTTON = (By.XPATH, '//button[text()="Создать"]')
    CREATE_MODULE_TITLE = (
        By.XPATH, '//*[contains(@id, "chakra-modal--header-:")]'
    )
    PRODUCT_TITLE = (By.CSS_SELECTOR, 'input[name="name"]')
    PRODUCT_PRICE = (By.CSS_SELECTOR, 'input[name="price"]')
    PRODUCT_DESCRIPTION = (By.CSS_SELECTOR, '[name="description"]')
    PRODUCT_IMAGE = (By.CSS_SELECTOR, 'input[name="imageUrl"]')
    SUBMIT_BUTTON = (By.XPATH, '//button[text()="Сохранить"]')
    SEARCH_FIELD = (
        By.CSS_SELECTOR, 'input[placeholder="Поиск по объявлениям"]'
    )
    SEARCH_BUTTON = (By.XPATH, '//button[text()="Найти"]')
    SEARCH_RESULTS = (By.XPATH, '//p[contains(text(), "Найдено: ")]')
    PRODUCT_CARD = (
        By.XPATH,
        f'//h4[contains(text(), {Constans.CREATE_PRODUCT_NAME})]'
    )
    EDIT_SAVE_BUTTON = (By.CSS_SELECTOR, 'svg[stroke="currentColor"]')
    DETAIL_PRODUCT_TITLE = (By.CSS_SELECTOR, 'h2.chakra-heading')
    DETAIL_PRODUCT_PRICE = (By.CSS_SELECTOR, 'header > p.chakra-text')
    DETAIL_PRODUCT_DESCRIPTION = (
        By.CSS_SELECTOR, '.chakra-stack > p.chakra-text'
    )
    DETAIL_PRODUCT_IMAGE = (By.CSS_SELECTOR, 'img[alt="product image"]')
