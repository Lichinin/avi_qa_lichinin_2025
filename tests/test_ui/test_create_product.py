from locators.locators import Selectors


def test_create_button(open_start_page):
    page = open_start_page
    page.click_button_create()
    page.assert_create_button_click()


def test_create_product(open_start_page):
    page = open_start_page
    page.click_button_create()
    page.paste_product_name(Selectors.CREATE_PRODUCT_NAME)
    page.paste_product_price(Selectors.CREATE_PRODUCT_PRICE)
    page.paste_product_description(Selectors.CREATE_PRODUCT_DESCRIPTION)
    page.paste_product_image(Selectors.CREATE_PRODUCT_DESCRIPTION)
    page.click_button_submit()
    page.find_product(Selectors.CREATE_PRODUCT_NAME)
    page.assert_create_product()
