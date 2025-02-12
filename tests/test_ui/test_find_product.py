from locators.locators import Selectors


def test_find_product(create_test_product, open_start_page):
    page = open_start_page
    page.find_product(Selectors.CREATE_PRODUCT_NAME)
    page.assert_find_product()

