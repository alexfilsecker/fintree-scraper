import datetime


class ScrapedMovement:
    def __init__(
        self, date: datetime.date, description: str, amount: int, balance: int
    ):
        self.date = date
        self.description = description
        self.amount = amount
        self.balance = balance

    def __repr__(self):
        return f"{self.amount}"

    def __str__(self):
        return f"{self.date}, {self.description}, {self.amount}, {self.balance}"
