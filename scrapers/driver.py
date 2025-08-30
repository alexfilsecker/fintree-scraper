from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from typing import Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from logger import logger


WAIT_TIME = 10


class Driver(webdriver.Chrome):
    def __init__(self, headless=True):
        self.headless = headless
        options = self._get_options()
        super().__init__(
            service=Service(ChromeDriverManager().install()), options=options
        )
        self.set_window_size(1920, 1080)
        logger.info("Initialized Chrome WebDriver")

    def _get_options(self):
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument("--headless")
            options.add_argument("--window-size=1920x1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return options

    def wait(self) -> WebDriverWait:
        return WebDriverWait(self, WAIT_TIME)

    def wait_clickable(self, element):
        self.wait().until(expected_conditions.element_to_be_clickable(element))

    def wait_visible(self, by: By, value: str):
        logger.info(f"waiting for visibility of element by {by}, {value}")
        self.wait().until(
            expected_conditions.visibility_of_element_located((by, value))
        )

    def click_element(self, element: WebElement):
        self.wait().until(expected_conditions.element_to_be_clickable(element))
        element.click()

    def click_by(self, by: By, value: str):
        logger.info(f"clicking by {by}, {value}")
        self.wait_visible(by, value)
        element = self.find_element(by=by, value=value)
        self.click_element(element)

    def send_keys_by(self, by: By, value: str, keys: str):
        logger.info(f"sending keys by {by}, {value}")
        element = self.find_element(by=by, value=value)
        element.send_keys(keys)

