from pydantic import BaseModel
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Dict, Tuple, List
import json



class FalabellaMovementInfo(BaseModel):
    amount: int
    total_amount: int
    current_installment: int
    total_installments: int
    shop: str
    industry: str
    iso_datetime: str
    country: str
    origin: str

    def __init__(self, data: Dict[str, str]):
        try:
            installments = self._get_installments(data["installments"])
            return super().__init__(
                amount=self._fix_amount(data["amount"]),
                total_amount=self._fix_amount(data["total_amount"]),
                current_installment=installments[0],
                total_installments=installments[1],
                shop=data["shop"],
                industry=data["industry"],
                iso_datetime=self._get_iso_datetime(data["date"], data["time"]),
                country=data["country"],
                origin=data["origin"],
            )
        except KeyError as e:
            raise ValueError(f"Missing required field: {e}") from e

    def _fix_amount(self, amount_str: str) -> int:
        return int(amount_str.replace(".", "").replace("$", "").replace(",", ""))

    def _get_installments(self, installments_str: str) -> Tuple[int, int]:
        installments = installments_str.split(" de ")
        return int(installments[0]), int(installments[1])

    def _get_iso_datetime(self, date_str: str, time_str: str) -> str:
        tmp_date = [int(item) for item in date_str.split("/")]
        tmp_date.reverse()
        tmp_time = [int(item) for item in time_str.split(":")]
        dt = datetime(*tmp_date, *tmp_time, tzinfo=ZoneInfo("America/Santiago"))
        return dt.isoformat()

    def __str__(self):
        dumped_dict = self.model_dump()
        json_str = json.dumps(dumped_dict, indent=4, ensure_ascii=False)
        return json_str


class FalabellaMovements(BaseModel):
    pending_movements: List[FalabellaMovementInfo] = []
    fulfilled_movements: List[FalabellaMovementInfo] = []

    def extend_movements(self, other: "FalabellaMovements"):
        if other.pending_movements:
            if self.pending_movements is None:
                self.pending_movements = []
            self.pending_movements.extend(other.pending_movements)
        self.fulfilled_movements.extend(other.fulfilled_movements)

    def __str__(self):
        dumped_dict = self.model_dump()
        json_str = json.dumps(dumped_dict, indent=4, ensure_ascii=False)
        return json_str