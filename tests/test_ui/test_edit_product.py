from locators.locators import Selectors


def test_edit_product(create_test_product, open_product_details_page):
    page = open_product_details_page
    page.click_button_edit()
    page.paste_product_name(Selectors.NEW_PRODUCT_NAME)
    page.paste_product_price(Selectors.NEW_PRODUCT_PRICE)
    page.paste_product_description(Selectors.NEW_PRODUCT_DESCRIPTION)
    page.paste_product_image(Selectors.NEW_PRODUCT_IMAGE)
    page.click_button_save_changes()
    page.assert_new_product()
