from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait

from typing import List


class Movement:
    def __init__(self, date: str, description: str, amount: int, balance: int):
        self.date = date
        self.description = description
        self.amount = amount
        self.balance = balance

    def __repr__(self):
        return f"{self.amount}"

    def __str__(self):
        return f"{self.date}, {self.description}, {self.amount}, {self.balance}"


class Scraper:

    url: str

    def __init__(self, rut: str, password: str, headles=True):
        self.rut = rut
        self.password = password
        self.headles = headles
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        if headles:
            options.add_argument("--headless")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )

    def wait_to_click(self, by: By, value: str) -> None:
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((by, value))
        )

    def find_element(self, by: By, value: str):
        return self.driver.find_element(by=by, value=value)

    def my_click(self, by: By, value: str) -> None:
        self.wait_to_click(by, value)
        self.find_element(by=by, value=value).click()

    def begin_scrap(self) -> None:
        self.driver.get(self.url)
        if self.headles:
            self.driver.set_window_size(1920, 1080)
        else:
            self.driver.maximize_window()

    def scrap(self) -> List[Movement]:
        pass
