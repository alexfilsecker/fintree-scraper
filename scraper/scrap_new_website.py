from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from typing import List

from src.scraper.scrap import Movement


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
