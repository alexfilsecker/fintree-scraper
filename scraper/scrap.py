from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait


from typing import List

from .scrap_new_website import scrap_new_website

from .scrap_utils import my_click, Movement


def scrap(rut: str, password: str) -> List[Movement]:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
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

    return scrap_new_website(driver)


if __name__ == "__main__":
    movements = scrap("200719913", "46@8sA5uqV")
    for movement in movements:
        print(movement)
