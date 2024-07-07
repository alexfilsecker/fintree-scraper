from .scrap import start_driver, my_click
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.remote.webdriver import WebDriver


class SantanderMovement:
    def __init__(self, date: str, description: str, ammount: int, balance: int):
        self.date = date
        self.description = description
        self.ammount = ammount
        self.balance = balance

    def __repr__(self):
        return f"{self.ammount}"

    def __str__(self):
        return f"{self.date}, {self.description}, {self.ammount}, {self.balance}"


def get_int_amount(amount: str) -> int:
    if amount == "":
        return 0
    return int(amount.replace(".", "").replace("$", ""))


def login_santander(driver: WebDriver, rut: str, password: str):
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


def scrap_santander(rut: str, password: str, headless: bool) -> List[SantanderMovement]:

    driver = start_driver(headless=headless)

    driver.get("https://banco.santander.cl/personas")

    login_santander(driver, rut, password)

    my_click(driver, By.XPATH, "//div[@id='user-guide-initiator']/div/button")

    my_click(
        driver,
        By.XPATH,
        "//app-container-accounts/div/div/mat-accordion/mat-expansion-panel/div/div/div",
    )

    WebDriverWait(driver, 10).until(
        expected_conditions.visibility_of_element_located(
            (By.TAG_NAME, "app-movimientos")
        )
    )

    moovements_app = driver.find_element(by=By.TAG_NAME, value="app-movimientos")

    WebDriverWait(driver, 10).until(
        expected_conditions.text_to_be_present_in_element(
            (By.XPATH, "//thead/tr/th"), "Fecha"
        )
    )

    table_body = moovements_app.find_element(by=By.TAG_NAME, value="tbody")

    rows = table_body.find_elements(by=By.TAG_NAME, value="tr")
    return_data = []
    for row in rows:
        data = [td.text for td in row.find_elements(by=By.TAG_NAME, value="td")]
        date = data[0]
        description = data[2]
        debit = get_int_amount(data[3])
        credit = get_int_amount(data[4])
        balance = get_int_amount(data[5])
        return_data.append(
            SantanderMovement(date, description, debit + credit, balance)
        )

    driver.quit()

    return return_data
