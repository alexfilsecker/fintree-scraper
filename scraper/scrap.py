from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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


def my_click(driver: WebDriver, by: By, value: str):
    WebDriverWait(driver, 10).until(
        expected_conditions.element_to_be_clickable((by, value))
    )
    driver.find_element(by=by, value=value).click()


def get_int_amount(amount: str) -> int:
    if amount == "":
        return 0
    return int(amount.replace(".", "").replace("$", ""))


def scrap(rut: str, password: str) -> List[Movement]:
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    driver.get("https://banco.santander.cl/personas")

    my_click(driver, By.CLASS_NAME, "btn-ingresar")

    rut_input_xpath = "//form[@class='s-login']/div/div/input"
    password_input_xpath = "//form[@class='s-login']/div[2]/div/input"
    login_btn_xpath = "//form[@class='s-login']/div[3]/button"

    WebDriverWait(driver, 10).until(
        expected_conditions.element_to_be_clickable((By.XPATH, rut_input_xpath))
    )

    rut_input = driver.find_element(by=By.XPATH, value=rut_input_xpath)
    password_input = driver.find_element(by=By.XPATH, value=password_input_xpath)

    rut_input.send_keys(rut)
    password_input.send_keys(password)

    my_click(driver, By.XPATH, login_btn_xpath)

    # scrap_new_website(driver)
    scrap_old_website(driver)


if __name__ == "__main__":
    movements = scrap("200719913", "46@8sA5uqV")
    for movement in movements:
        print(movement)
