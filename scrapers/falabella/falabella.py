from ..driver import Driver
from models.credentials import FalabellaCredentials
from logger import logger
from .login_falabella import LoginFalabellaScraper
from .private_navigator_falabella import PrivateNavigatorFalabella
from .cmr_falabella import CMRFalabella
from services import mongo_service
from config.constants import Collections


class FalabellaScraper:
    collection = Collections.FALABELLA_COLLECTION

    def __init__(self, driver: Driver, creds: FalabellaCredentials):
        self.driver = driver
        self.login_scraper = LoginFalabellaScraper(driver, creds)
        self.private_navigator = PrivateNavigatorFalabella(driver)
        self.cmr_scraper = CMRFalabella(driver)

    def scrap(self):
        try:
            self.login_scraper.login()
            self.private_navigator.go_to_cmr()
            movements = self.cmr_scraper.scrap_cmr()
            mongo_service.upload_document(self.collection, movements.model_dump())

        except Exception as e:
            logger.error("Failed to scrap")
            logger.error(e)
        else:
            logger.info("Scrap successful")
        finally:
            pass
            # self.driver.quit()
