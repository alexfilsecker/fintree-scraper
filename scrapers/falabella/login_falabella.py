from models.credentials import FalabellaCredentials
from scrapers.driver import Driver
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class LoginFalabellaScraper:
    BASE_URL = "https://www.bancofalabella.cl/"
    MY_ACCOUNT_BUTTON_XPATH = "//nav//button[3]"
    RUT_INPUT_XPATH = "(//nav//input)[1]"
    PASSWORD_INPUT_XPATH = "(//nav//input)[2]"
    LOGIN_BUTTON_ID = "desktop-login"
    UNKNOWN_ERROR_URL = "https://www.bancofalabella.cl/?errorMessage=UNKNOWN_ERROR"
    MAX_LOGIN_TRIES = 1000
    LOGIN_ERROR_MODAL_CLOSE_XPATH = '//*[@id="modal-message"]/div[2]/div[1]'
    OMNI_2_URL = "https://web2.bancofalabella.cl/web-clientes/techbank-client"

    def __init__(self, driver: Driver, creds: FalabellaCredentials):
        self.driver = driver
        self.creds = creds

    def login(self):
        self.driver.get(self.BASE_URL)
        self._recursive_login()

    def _recursive_login(self, tries=0):
        if tries > self.MAX_LOGIN_TRIES:
            raise RecursionError()

        self._login()
        success = self._check_login()
        if success:
            return

        self.driver.click_by(By.XPATH, self.LOGIN_ERROR_MODAL_CLOSE_XPATH)

        self._recursive_login(tries + 1)

    def _login(self):
        self.driver.wait_visible(By.XPATH, self.MY_ACCOUNT_BUTTON_XPATH)
        time.sleep(1)
        self.driver.click_by(By.XPATH, self.MY_ACCOUNT_BUTTON_XPATH)
        print("Clicked login button")

        # force wait 1 second
        time.sleep(1)
        self.driver.click_by(By.XPATH, self.RUT_INPUT_XPATH)
        self.driver.send_keys_by(By.XPATH, self.RUT_INPUT_XPATH, self.creds.rut)
        self.driver.click_by(By.XPATH, self.PASSWORD_INPUT_XPATH)
        self.driver.send_keys_by(
            By.XPATH, self.PASSWORD_INPUT_XPATH, self.creds.password
        )

        self.driver.click_by(By.ID, self.LOGIN_BUTTON_ID)

    def _check_login(self) -> bool:
        self.driver.wait().until(
            EC.any_of(
                EC.url_to_be(self.UNKNOWN_ERROR_URL), EC.url_to_be(self.OMNI_2_URL)
            )
        )

        if self.driver.current_url == self.OMNI_2_URL:
            return True

        if self.driver.current_url == self.UNKNOWN_ERROR_URL:
            return False

        raise ValueError()
