from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By


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


def my_click(driver: WebDriver, by: By, value: str):
    WebDriverWait(driver, 10).until(
        expected_conditions.element_to_be_clickable((by, value))
    )
    driver.find_element(by=by, value=value).click()


def get_int_amount(amount: str) -> int:
    if amount == "":
        return 0
    return int(amount.replace(".", "").replace("$", ""))
