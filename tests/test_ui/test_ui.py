from locators.locators import Selectors


def test_ui(open_start_page):
    page = open_start_page
    page.get_element(Selectors.DYNAMIC).click()
    assert "Dynamic" in page.browser.title


def test_ui_broken(open_start_page):
    page = open_start_page
    page.get_element(Selectors.DYNAMIC).click()
    assert "Broken" in page.browser.title
