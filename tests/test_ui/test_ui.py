from locators.locators import Selectors
import pytest


def test_ui(open_start_page):
    page = open_start_page
    page.get_element(Selectors.DYNAMIC).click()
    assert "Dynamic" in page.browser.title

@pytest.mark.xfail(reason='Намеренный провал')
def test_ui_broken(open_start_page):
    page = open_start_page
    page.get_element(Selectors.DYNAMIC).click()
    assert "Broken" in page.browser.title
