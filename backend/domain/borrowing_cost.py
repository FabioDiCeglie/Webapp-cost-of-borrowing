from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class BorrowingCost:
    period_date: date
    value: Decimal

