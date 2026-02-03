from datetime import datetime, timezone
from ..driver import Driver
from models.credentials import FalabellaCredentials
from logger import logger
from .login_falabella import LoginFalabellaScraper
from .private_navigator_falabella import PrivateNavigatorFalabella
from .cmr_falabella import CMRFalabella
from services import mongo_service
from config.constants import Collections
import traceback


class FalabellaScraper:
    collection = Collections.FALABELLA_COLLECTION

    def __init__(self, driver: Driver, creds: FalabellaCredentials):
        self.driver = driver
        self.login_scraper = LoginFalabellaScraper(driver, creds)
        self.private_navigator = PrivateNavigatorFalabella(driver)
        self.cmr_scraper = CMRFalabella(driver)

    def scrap(self):
        try:
            start_time = datetime.now(timezone.utc)
            self.login_scraper.login()
            self.private_navigator.go_to_cmr()
            movements = self.cmr_scraper.scrap_cmr()
            end_time = datetime.now(timezone.utc)
            duration = end_time - start_time
            mongo_document = {
                **movements.model_dump(),
                "scrap_start_time": start_time,
                "scrap_end_time": end_time,
            }
            mongo_service.upload_document(self.collection, mongo_document)

        except Exception as e:
            traceback.print_exc()
            logger.error("Failed to scrap")
            logger.error(e)
        else:
            logger.info("Scrap successful")
        finally:
            pass
            # self.driver.quit()
