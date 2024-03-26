from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from typing import List
from selenium.webdriver.support.ui import WebDriverWait

from .scraper import Scraper, Movement

import time


class SantanderScraper(Scraper):

    url = "https://banco.santander.cl/personas"

    def scrap(self) -> None:
        self.begin_scrap()
        self.login()
        old_page = self.check_for_old_page()
        if old_page:
            movements = self.scrap_old_page()
        else:
            movements = self.scrap_new_page()

        self.driver.quit()

        for movement in movements:
            print(movement)

        return movements

    def login(self) -> None:
        self.my_click(By.ID, "btnIngresar")

        form_xpath = "//form[@class='s-login pt-28']"
        rut_input_xpath = f"{form_xpath}/div/div/input"
        password_input_xpath = f"{form_xpath}/div[2]/div/input"
        login_btn_xpath = f"{form_xpath}/div[3]/button"

        self.wait_to_click(By.XPATH, rut_input_xpath)

        rut_input = self.find_element(by=By.XPATH, value=rut_input_xpath)
        password_input = self.find_element(by=By.XPATH, value=password_input_xpath)

        rut_input.send_keys(self.rut)
        password_input.send_keys(self.password)

        self.my_click(By.XPATH, login_btn_xpath)

    def check_for_old_page(self) -> bool:
        return False

    def scrap_old_page(self) -> List[Movement]:
        self.go_to_frame_2()
        self.go_to_last_movements()
        self.access_frame_p4()

    def go_to_frame_2(self):
        self.driver.switch_to.frame("frame2")

    def access_frame_p4(self):
        hola = self.driver.find_elements(By.TAG_NAME, "div")
        print(hola)
        # self.driver.switch_to.parent_frame()
        self.driver.switch_to.frame("p4")
        time.sleep(1)
        hola = self.driver.find_elements(By.TAG_NAME, "div")
        print(hola)

    def go_to_last_movements(self):
        self.my_click(By.ID, "CU1")
        self.my_click(By.ID, "CC2")
        self.my_click(By.ID, "UM3")

    def scrap_new_page(self) -> List[Movement]:
        self.close_greeter()
        self.click_on_first_account()
        self.wait_for_movements()
        return self.get_last_movements()

    def close_greeter(self) -> None:
        self.my_click(By.XPATH, "//app-user-guide-initiator/div/em")

    def click_on_first_account(self) -> None:
        self.my_click(
            By.XPATH,
            "//app-container-accounts/div/div/mat-accordion/mat-expansion-panel/div/div/div",
        )

    def wait_for_movements(self) -> None:
        WebDriverWait(self.driver, 10).until(
            expected_conditions.text_to_be_present_in_element(
                (By.XPATH, "//thead/tr/th"), "Fecha"
            )
        )

    def get_last_movements(self):
        moovements_app = self.find_element(by=By.TAG_NAME, value="app-movimientos")
        table_body = moovements_app.find_element(by=By.TAG_NAME, value="tbody")

        def get_int_amount(amount: str) -> int:
            if amount == "":
                return 0
            return int(amount.replace(".", "").replace("$", ""))

        rows = table_body.find_elements(by=By.TAG_NAME, value="tr")
        movements: List[Movement] = []
        for row in rows:
            data = [td.text for td in row.find_elements(by=By.TAG_NAME, value="td")]
            date = data[0]
            description = data[2]
            debit = get_int_amount(data[3])
            credit = get_int_amount(data[4])
            balance = get_int_amount(data[5])
            movements.append(Movement(date, description, debit + credit, balance))

        return movements
