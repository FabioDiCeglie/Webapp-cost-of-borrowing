from datetime import date
from decimal import Decimal

from domain.time_series import TimeSeriesObservation
from services.cost_of_borrowing_households.service import CostOfBorrowingHouseholdsService


class FakeProvider:
    def __init__(self, observations: list[TimeSeriesObservation]) -> None:
        self._observations = observations

    def fetch_observations(self) -> list[TimeSeriesObservation]:
        return list(self._observations)


class FakeRepository:
    def __init__(self, *, observations_to_return: list[TimeSeriesObservation] | None = None) -> None:
        self.last: list[TimeSeriesObservation] | None = None
        self.last_range: tuple[date | None, date | None] | None = None
        self._observations_to_return: list[TimeSeriesObservation] = list(observations_to_return or [])

    def upsert_observations(self, db, observations: list[TimeSeriesObservation]) -> int:
        self.last = list(observations)
        return len(observations)

    def get_observations(self, db, *, start: date | None = None, end: date | None = None):
        self.last_range = (start, end)
        return list(self._observations_to_return)


def test_ingest_fetches_and_upserts() -> None:
    observations = [
        TimeSeriesObservation(period_date=date(2026, 1, 1), value=Decimal("3.35")),
        TimeSeriesObservation(period_date=date(2026, 2, 1), value=Decimal("3.30")),
    ]
    provider = FakeProvider(observations)
    repo = FakeRepository()
    service = CostOfBorrowingHouseholdsService(provider, repo)

    ingested = service.ingest(db=None)

    assert ingested == 2
    assert repo.last == observations


def test_get_observations_delegates_to_repository() -> None:
    provider = FakeProvider([])
    expected = [TimeSeriesObservation(period_date=date(2026, 1, 1), value=Decimal("3.35"))]
    repo = FakeRepository(observations_to_return=expected)
    service = CostOfBorrowingHouseholdsService(provider, repo)

    start = date(2022, 1, 1)
    end = date(2026, 1, 1)
    got = service.get_observations(db=None, start=start, end=end)

    assert got == expected
    assert repo.last_range == (start, end)

