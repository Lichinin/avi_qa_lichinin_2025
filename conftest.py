import datetime
import logging
import logging.handlers
from logging.handlers import RotatingFileHandler
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver

from constants.constants import Constans
from pages.details_page import DetailsPage
from pages.products_page import ProductPage


def pytest_addoption(parser):
    parser.addoption('--browser', action='store', default='firefox')
    parser.addoption('--url', action='store', default='http://tech-avito-intern.jumpingcrab.com')
    parser.addoption('--log_level', action='store', default="INFO")
    parser.addoption('--executor', action='store')
    parser.addoption('--browser_version', action='store')


@pytest.fixture(scope='function')
def logger(request):
    log_dir = Path(__file__).parent / 'log'
    log_dir.mkdir(exist_ok=True)
    log_level = request.config.getoption('--log_level')
    browser_name = request.config.getoption('--browser')
    logger = logging.getLogger(request.node.name)
    file_handler = RotatingFileHandler(
        str(log_dir / f'{request.node.name}({browser_name}).log'),
        maxBytes=30000000,
        backupCount=3)
    file_handler.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
    logger.addHandler(file_handler)
    logger.setLevel(level=log_level)

    logger.info('===> Test %s started at %s' % (request.node.name, datetime.datetime.now()))

    yield logger

    logger.info('===> Test %s finished at %s' % (request.node.name, datetime.datetime.now()))

    for handler in logger.handlers:
        handler.close()
    logger.handlers.clear()


@pytest.fixture()
def browser(request, logger) -> WebDriver:
    browser_name = request.config.getoption('--browser')
    browser_version = request.config.getoption('--browser_version')
    executor = request.config.getoption('--executor')
    url = request.config.getoption('--url')

    if executor:
        if browser_name == 'chrome':
            options = ChromeOptions()
            options.page_load_strategy = 'eager'
        elif browser_name == 'firefox':
            options = FirefoxOptions()
            options.page_load_strategy = 'eager'
        elif browser_name == 'edge':
            options = EdgeOptions()
            options.page_load_strategy = 'eager'
        else:
            raise ValueError(
                'Browser name must be "chrome", "firefox" or "edge"'
            )
        options.headless = False
        capabilities = {
            'browserName': browser_name,
            'browserVersion': browser_version,
            'selenoid:options': {
                'enableVNC': True,
            },
        }
        for key, value in capabilities.items():
            options.set_capability(key, value)

        driver = webdriver.Remote(
            command_executor=f'http://{executor}:4444/wd/hub',
            options=options
        )
        driver.maximize_window()
    else:
        if browser_name == 'chrome':
            options = webdriver.ChromeOptions()
            options.add_argument("--headless=new")
            driver = webdriver.Chrome(options=options)
        elif browser_name == 'firefox':
            options = webdriver.FirefoxOptions()
            options.add_argument("--start-maximized")
            options.page_load_strategy = 'eager'
            # options.add_argument("--headless")
            driver = webdriver.Firefox(options=options)
            # driver.fullscreen_window()
        elif browser_name == 'edge':
            options = webdriver.EdgeOptions()
            options.use_chromium = True
            options.add_argument("--headless=new")
            driver = webdriver.Edge(options=options)
        else:
            raise ValueError(
                'Browser name must be "chrome", "firefox" or "edge"'
            )
    driver.get(url)
    driver.url = url
    driver.logger = logger
    driver.test_name = request.node.name

    logger.info("Browser %s v. %s started" % (browser_name, browser_version))

    yield driver
    driver.quit()


@pytest.fixture()
def open_start_page(browser) -> ProductPage:
    return ProductPage(browser)


@pytest.fixture()
def open_product_details_page(browser) -> DetailsPage:
    page = DetailsPage(browser)
    page.find_product(Constans.CREATE_PRODUCT_NAME)
    page.click_product_card()
    return page


@pytest.fixture()
def create_test_product(open_start_page):
    page = open_start_page
    page.click_button_create()
    page.paste_product_name(Constans.CREATE_PRODUCT_NAME)
    page.paste_product_price(Constans.CREATE_PRODUCT_PRICE)
    page.paste_product_description(Constans.CREATE_PRODUCT_DESCRIPTION)
    page.paste_product_image(Constans.CREATE_PRODUCT_IMAGE)
    page.click_button_submit()
