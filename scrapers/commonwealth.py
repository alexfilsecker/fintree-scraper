from .scrap import start_driver, my_click
from typing import List, Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime


class CommonWealthMovement:
    def __init__(
        self,
        date: str,
        value_date: str,
        description: str,
        ammount: float,
        balance: float | None = None,
    ):
        self.date = format_date(date)
        self.value_date = format_date(value_date)
        self.description = description
        self.ammount = ammount
        self.balance = balance

    def __repr__(self):
        return f"{self.ammount}"

    def __str__(self):
        return f"{self.date}, {self.description}, {self.ammount}, {self.balance}"


def get_float_ammount(ammount: str) -> int:
    return float(ammount.replace("$", "").replace(",", ""))


def format_date(date: str) -> str:
    if date.find("/") != -1:
        return date
    date_object = datetime.strptime(date, "%a %d %b %Y")
    return date_object.strftime("%d/%m/%Y")


def login_commonwealth(driver: WebDriver, client_number: str, password: str):
    client_number_id = "txtMyClientNumber_field"
    my_click(driver, By.ID, client_number_id)
    client_number_input = driver.find_element(by=By.ID, value=client_number_id)
    client_number_input.send_keys(client_number)

    password_id = "txtMyPassword_field"
    my_click(driver, By.ID, password_id)
    password_input = driver.find_element(by=By.ID, value=password_id)
    password_input.send_keys(password)

    login_btn_id = "btnLogon_field"
    my_click(driver, By.ID, login_btn_id)


def access_smart_access(driver: WebDriver):
    smart_access_xpath = "//*[@id='StartMainContent']/div/div[2]/div[1]/main/section[1]/div/div[1]/div/div/div[1]/div[2]/div/div/div/a"
    my_click(driver, By.XPATH, smart_access_xpath)

    WebDriverWait(driver, 10).until(
        expected_conditions.visibility_of_element_located(
            (By.XPATH, '//*[@id="transaction-list"]/div[2]/span')
        )
    )


def scrap_transactions(
    transaction_rows: List[WebElement], pending: bool, date: str = None
) -> List[CommonWealthMovement]:
    movements = []
    for transaction in transaction_rows:
        # Skip hidden rows
        if transaction.get_attribute("aria-hidden") == "true":
            continue

        # Get data from row
        data = transaction.find_elements(by=By.TAG_NAME, value="td")

        # Get date and description
        date_and_description = data[0]
        try:
            date_and_description_element = date_and_description.find_element(
                by=By.XPATH, value=".//button/div/div[2]/div"
            )
        except NoSuchElementException:
            date_and_description_element = date_and_description.find_element(
                by=By.XPATH, value=".//span"
            )

        date_and_description = date_and_description_element.text
        if pending:
            date = date_and_description.split("\n")[0]
            description = date_and_description.split("\n")[1].split("PENDING: ")[1]
            value_date = date
        else:
            splited_description = date_and_description.split("Value Date: ")
            if len(splited_description) > 1:
                description = splited_description[0]
                value_date = splited_description[1]
            else:
                description = date_and_description
                value_date = date

        # Get ammounts
        ammounts = []
        ammounts_element = data[1]
        spans = ammounts_element.find_elements(by=By.XPATH, value="./*")
        for span in spans:
            if len(span.find_elements(by=By.TAG_NAME, value="span")) == 0:
                ammounts.append(0)
            else:
                ammount_element = span.find_element(
                    by=By.XPATH, value=".//span/span/span"
                )
                ammount = ammount_element.text
                ammounts.append(get_float_ammount(ammount))

        if ammounts[0] == 0:
            ammount = ammounts[1]
        else:
            ammount = ammounts[0]

        if pending:
            balance = None
        else:
            balance = ammounts[2]

        movements.append(
            CommonWealthMovement(date, value_date, description, ammount, balance)
        )

    return movements


def scrap_pending_transactions(
    driver: WebDriver,
) -> Tuple[int, List[CommonWealthMovement]]:
    pending_transaction_table_id = "pending-transactions-table"
    try:
        pending_transaction_table = driver.find_element(
            by=By.ID, value=pending_transaction_table_id
        )
    except NoSuchElementException:
        return (0, [])

    pendign_transaction_table_body = pending_transaction_table.find_element(
        by=By.TAG_NAME, value="tbody"
    )
    pending_transaction_rows = pendign_transaction_table_body.find_elements(
        by=By.TAG_NAME, value="tr"
    )
    total_pending_element = pending_transaction_rows.pop(0)
    total_pending_span = total_pending_element.find_element(
        by=By.XPATH, value=".//td/span/span"
    )
    total_pending_value = get_float_ammount(total_pending_span.text)

    movements = scrap_transactions(pending_transaction_rows, pending=True)
    return total_pending_value, movements


def scrap_non_pending_transactions(driver: WebDriver) -> List[CommonWealthMovement]:
    table_id = "non-pending-transactions-table"
    non_pending_table = driver.find_element(by=By.ID, value=table_id)
    table_bodys = non_pending_table.find_elements(by=By.TAG_NAME, value="tbody")
    movements: List[CommonWealthMovement] = []
    for table_body in table_bodys:
        transaction_rows = table_body.find_elements(by=By.TAG_NAME, value="tr")
        date_row = transaction_rows.pop(0)
        date_element = date_row.find_element(by=By.XPATH, value=".//td/span")
        date = date_element.text
        new_movements = scrap_transactions(transaction_rows, pending=False, date=date)
        movements.extend(new_movements)

    return movements


def scrap_commonwealth(
    client_number: str, password: str, headless: bool
) -> Tuple[int, List[CommonWealthMovement], List[CommonWealthMovement]]:
    driver = start_driver(headless=headless)
    driver.get("https://www.my.commbank.com.au/netbank/Logon/Logon.aspx?ei=mv_logon-NB")

    login_commonwealth(driver, client_number, password)
    access_smart_access(driver)
    total_pending, pending_movements = scrap_pending_transactions(driver)
    non_pending_movements = scrap_non_pending_transactions(driver)

    return (total_pending, pending_movements, non_pending_movements)
