from __future__ import annotations

from abc import ABC, abstractmethod

from domain.borrowing_cost import BorrowingCost


class BorrowingCostProvider(ABC):
    @abstractmethod
    def fetch_observations(self) -> list[BorrowingCost]:
        return ...

