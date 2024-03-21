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


def scrap_new_website(driver: WebDriver) -> List[Movement]:
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
    return_data: List[Movement] = []
    for row in rows:
        data = [td.text for td in row.find_elements(by=By.TAG_NAME, value="td")]
        date = data[0]
        description = data[2]
        debit = get_int_amount(data[3])
        credit = get_int_amount(data[4])
        balance = get_int_amount(data[5])
        return_data.append(Movement(date, description, debit + credit, balance))

    driver.quit()

    for movement in return_data:
        print(movement)

    return return_data


if __name__ == "__main__":
    movements = scrap("200719913", "46@8sA5uqV")
    for movement in movements:
        print(movement)
