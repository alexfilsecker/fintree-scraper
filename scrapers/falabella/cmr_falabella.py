from typing import List, Dict
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.shadowroot import ShadowRoot
from ..driver import Driver
import time
from logger import logger
from models.movements.falabella_movement import (
    FalabellaMovementInfo,
    FalabellaMovements,
)


class CMRFalabella():
    CREDIT_MOVEMENTS_XPATH = "//credit-card-movements"
    MOVEMENTS_MODAL_TAG = "modalDetailTransaction"
    MOVEMENTS_MODAL_TEXT_XPATH = ".//div[1]"

    FIND_MODAL_MAX_TRIES = 30
    FIND_MODAL_DELAY_MS = 100


    MODAL_TITLE_XPATH = ".//h4"
    MODAL_AMOUNT_XPATH = "./div[3]"
    MODAL_CONTENT_XPATH = "./div[4]"
    MODAL_CONTENT_MAPPING = {
        "Monto total": "total_amount",
        "Cuotas": "installments",
        "Comercio": "shop",
        "Rubro": "industry",
        "Fecha": "date",
        "Hora": "time",
        "Pais": "country",
        "Origen de la compra": "origin",
    }


    def __init__(self, driver: Driver):
        self.driver = driver

    def _wait_loader(self):
        self.driver.wait().until(
            EC.visibility_of_element_located((By.TAG_NAME, "app-loader"))
        )
        self.driver.wait().until(
            EC.invisibility_of_element_located((By.TAG_NAME, "app-loader"))
        )

    def scrap_cmr(self) -> FalabellaMovements:
        self.shadow_root = self._get_shadow_root()
        all_movements = FalabellaMovements()
        while True:
            tables = self._get_movement_tables()
            other_movements = self._get_all_movements(tables)
            all_movements.extend_movements(other_movements)
            break
    
        return all_movements

    def _get_shadow_root(self) -> ShadowRoot:
        self.driver.wait().until(
            EC.presence_of_element_located((By.XPATH, self.CREDIT_MOVEMENTS_XPATH))
        )
        movements_host = self.driver.find_element(
            by=By.XPATH, value=self.CREDIT_MOVEMENTS_XPATH
        )
        shadow_root = self.driver.execute_script(
            "return arguments[0].shadowRoot", movements_host
        )

        if not shadow_root:
            raise Exception("Could not access shadow root")

        return shadow_root

    def _get_movement_tables(self) -> List[WebElement]:
        tables = self.driver.execute_script(
            """
            const root = arguments[0];
            return Array.from(root.querySelectorAll('table'));
            """,
            self.shadow_root,
        )

        print(f"Found {len(tables)} tables in shadow root")

        if len(tables) == 0:
            raise Exception("There are no tables to scrap")

        if len(tables) > 2:
            raise Exception("WTF there are more than two tables")

        return tables

    def _get_all_movements(self, tables: List[WebElement]):
        pending_table = None
        pending_movements = []
        if len(tables) == 2:
            pending_table = tables[0]
            fulfilled_table = tables[1]

        else:
            fulfilled_table = tables[0]

        if pending_table:
            pending_movements = self._get_movements_from_table(pending_table)
        fulfilled_movements = self._get_movements_from_table(fulfilled_table)

        return FalabellaMovements(
            pending_movements=pending_movements, fulfilled_movements=fulfilled_movements
        )

    def _get_movements_from_table(self, table: WebElement):
        tbody = table.find_element(by=By.TAG_NAME, value="tbody")
        rows = tbody.find_elements(by=By.TAG_NAME, value="tr")
        movements: List[FalabellaMovementInfo] = []
        for row in rows:
            self.driver.click_element(row)
            self._wait_loader()
            movement = self._scrap_movements_modal()
            movements.append(movement)
            logger.info(f"Scraped movement: {movement}")
        return movements

    def _scrap_movements_modal(self):
        modal = self._find_modal()

        modal_div = modal.find_element(By.XPATH, "./div/div")

        title_element = modal_div.find_element(By.XPATH, self.MODAL_TITLE_XPATH)
        title_value = title_element.text.strip()

        amount_element = modal_div.find_element(By.XPATH, self.MODAL_AMOUNT_XPATH)
        amount_value = amount_element.text.strip()

        data = {
            "title": title_value,
            "amount": amount_value
        }

        content_div = modal_div.find_element(By.XPATH, self.MODAL_CONTENT_XPATH)
        self._scrap_modal_content_div(content_div, data)

        movement_object = FalabellaMovementInfo(data)

        modal.find_element(By.XPATH, ".//button").click()
        return movement_object

    def _scrap_modal_content_div(self, content_div: WebElement, data: Dict[str, str]):
        content_elements = content_div.find_elements(By.TAG_NAME, "div")

        for element in content_elements:
            element_class = element.get_attribute("class")
            if element_class != "pair":
                continue

            element_key_span = element.find_element(By.XPATH, "./span[1]")
            element_key_value = element_key_span.text.strip()

            if element_key_value not in self.MODAL_CONTENT_MAPPING:
                continue

            data_key = self.MODAL_CONTENT_MAPPING[element_key_value]
            element_value_span = element.find_element(By.XPATH, "./span[2]")
            element_value = element_value_span.text.strip()
            data[data_key] = element_value


    def _find_modal(self, attempt=0) -> WebElement:
        if attempt > self.FIND_MODAL_MAX_TRIES:
            raise Exception(
                f"Could not find modal after {self.FIND_MODAL_MAX_TRIES} attempts"
            )

        modal = self.driver.execute_script(
            """
            const root = arguments[0];
            return root.querySelector('app-modal-detail');
            """,
            self.shadow_root,
        )
        if not isinstance(modal, WebElement):
            time.sleep(self.FIND_MODAL_DELAY_MS / 1000)
            return self._find_modal(attempt + 1)

        return modal

    def _get_next_page_button(self) -> WebElement:
        app_last_movements = self.driver.execute_script(
            """
            const root = arguments[0];
            return root.querySelector('app-last-movements');
            """,
            self.shadow_root,
        )

        if not isinstance(app_last_movements, WebElement):
            raise Exception("app last movements not found")
        
        buttons = app_last_movements.find_elements(By.TAG_NAME, "button")
        if len(buttons) < 2:
            raise Exception("not enough buttons")
        
        next_button = buttons[1]
        return next_button

