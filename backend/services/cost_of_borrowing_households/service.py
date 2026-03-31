from datetime import date

from sqlalchemy.orm import Session

from ports.time_series_provider import TimeSeriesProvider
from repositories.time_series_repository import TimeSeriesObservationRepository


class CostOfBorrowingHouseholdsService:
    def __init__(self, provider: TimeSeriesProvider, repository: TimeSeriesObservationRepository) -> None:
        self._provider = provider
        self._repository = repository

    def ingest(self, db: Session) -> int:
        observations = self._provider.fetch_observations()
        return self._repository.upsert_observations(db, observations)

    def get_observations(
        self,
        db: Session,
        *,
        start: date | None = None,
        end: date | None = None,
    ):
        return self._repository.get_observations(db, start=start, end=end)

