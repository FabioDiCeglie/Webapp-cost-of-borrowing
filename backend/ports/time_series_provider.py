from __future__ import annotations

from abc import ABC, abstractmethod

from domain.time_series import TimeSeriesObservation


class TimeSeriesProvider(ABC):
    @abstractmethod
    def fetch_observations(self) -> list[TimeSeriesObservation]:
        return ...

