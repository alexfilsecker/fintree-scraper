from scrapers.driver import Driver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
import time


def wait_loader_wrapper(func):
    def wrapper(navigator: "PrivateNavigatorFalabella", *args, **kwargs):
        navigator.wait_loader()
        result = func(navigator, *args, **kwargs)
        navigator.wait_loader()
        return result
    return wrapper

class PrivateNavigatorFalabella:
    BASE_PRIVATE_URL = "https://web2.bancofalabella.cl/web-clientes/techbank-client"
    CMR_BUTTON_XPATH = "//app-credit-cards//div[@class='product-center']"
    MODAL_CLOSE_XPATH = "//app-modals-campaigns//button"

    def __init__(self, driver: Driver):
        self.driver = driver
    
    def wait_loader(self):
        self.driver.wait().until(
            EC.visibility_of_element_located((By.TAG_NAME, "app-loader"))
        )
        self.driver.wait().until(
            EC.invisibility_of_element_located((By.TAG_NAME, "app-loader"))
        )
    
    @wait_loader_wrapper
    def go_to_cmr(self):
        if self.driver.current_url != self.BASE_PRIVATE_URL:
            self.driver.get(self.BASE_PRIVATE_URL)

        try:
            self.driver.click_by(By.XPATH, self.CMR_BUTTON_XPATH)
        # Except exception where the click would be intercepted by a modal
        except ElementClickInterceptedException:
            self.driver.click_by(By.XPATH, self.MODAL_CLOSE_XPATH)
            time.sleep(1)
            self.driver.click_by(By.XPATH, self.CMR_BUTTON_XPATH)
