from selenium.webdriver.common.by import By


class Selectors:

    CREATE_PRODUCT_NAME = 'f731'
    CREATE_PRODUCT_PRICE = '1000'
    CREATE_PRODUCT_DESCRIPTION = 'description'
    CREATE_PRODUCT_IMAGE = 'image'

    NEW_PRODUCT_NAME = 'f73.v2'
    NEW_PRODUCT_PRICE = '2000'
    NEW_PRODUCT_DESCRIPTION = 'new_description'
    NEW_PRODUCT_IMAGE = 'new_image'

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
    PRODUCT_CARD = (By.XPATH, '//h4[text()="f731"]')
    EDIT_SAVE_BUTTON = (By.CSS_SELECTOR, 'svg[stroke="currentColor"]')
    DETAIL_PRODUCT_TITLE = (By.CSS_SELECTOR, 'h2.chakra-heading')
    DETAIL_PRODUCT_PRICE = (By.CSS_SELECTOR, 'header > p.chakra-text')
    DETAIL_PRODUCT_DESCRIPTION = (
        By.CSS_SELECTOR, '.chakra-stack > p.chakra-text'
    )
    DETAIL_PRODUCT_IMAGE = (By.CSS_SELECTOR, 'img[alt="product image"]')
