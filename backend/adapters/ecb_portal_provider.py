import os
from datetime import date
from decimal import Decimal, InvalidOperation

import httpx

from domain.time_series import TimeSeriesObservation
from ports.time_series_provider import TimeSeriesProvider


class EcbPortalProvider(TimeSeriesProvider):
    def __init__(self) -> None:
        self._base_url = os.environ.get("ECB_PORTAL_BASE_URL", "https://data.ecb.europa.eu").rstrip("/")
        self._series_key = os.environ.get("ECB_SERIES_KEY")
        if not self._series_key:
            raise RuntimeError("ECB_SERIES_KEY is required but was not set")

    def _parse_observation(self, row: object) -> TimeSeriesObservation | None:
        if not isinstance(row, dict):
            return None
        # We only ingest monthly observations
        if row.get("FREQUENCY") != "M":
            return None
        period_raw = row.get("PERIOD")
        value_raw = row.get("OBS_VALUE_AS_IS") or row.get("OBS")
        if not period_raw or value_raw is None:
            return None
        try:
            return TimeSeriesObservation(
                period_date=date.fromisoformat(str(period_raw)),
                value=Decimal(str(value_raw)),
            )
        except (ValueError, InvalidOperation):
            return None

    def fetch_observations(self) -> list[TimeSeriesObservation]:
        url = f"{self._base_url}/data-detail-api/{self._series_key}"

        try:
            resp = httpx.get(url, headers={"Accept": "application/json"}, timeout=30.0)
            resp.raise_for_status()
        except httpx.HTTPError as e:
            raise RuntimeError(f"Failed to fetch ECB observations from {url}") from e

        try:
            payload = resp.json()
        except ValueError as e:
            raise RuntimeError(f"ECB response was not valid JSON from {url}") from e

        observations: list[TimeSeriesObservation] = []
        for row in payload:
            observation = self._parse_observation(row)
            if observation is not None:
                observations.append(observation)

        observations.sort(key=lambda p: p.period_date)
        return observations

