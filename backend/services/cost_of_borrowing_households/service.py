from sqlalchemy.orm import Session

from ports.time_series_provider import TimeSeriesProvider
from repositories.time_series_repository import TimeSeriesRepository


class IngestCostOfBorrowingHouseholdsService:
    def __init__(self, provider: TimeSeriesProvider, repository: TimeSeriesRepository) -> None:
        self._provider = provider
        self._repository = repository

    def ingest(self, db: Session) -> int:
        observations = self._provider.fetch_observations()
        return self._repository.upsert_observations(db, observations)

