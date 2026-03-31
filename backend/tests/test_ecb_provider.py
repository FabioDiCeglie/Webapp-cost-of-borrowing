import os
from datetime import date
from decimal import Decimal
from types import SimpleNamespace

import httpx

from adapters.ecb_portal_provider import EcbPortalProvider


def test_parse_observation_monthly() -> None:
    os.environ["ECB_SERIES_KEY"] = "dummy"
    provider = EcbPortalProvider()

    obs = provider._parse_observation(
        {"FREQUENCY": "M", "PERIOD": "2026-01-01", "OBS_VALUE_AS_IS": "3.35"}
    )

    assert obs is not None
    assert obs.period_date == date(2026, 1, 1)
    assert obs.value == Decimal("3.35")


def test_parse_observation_ignores_non_monthly() -> None:
    os.environ["ECB_SERIES_KEY"] = "dummy"
    provider = EcbPortalProvider()

    obs = provider._parse_observation(
        {"FREQUENCY": "D", "PERIOD": "2026-01-01", "OBS_VALUE_AS_IS": "3.35"}
    )

    assert obs is None


def test_fetch_observations_parses_filters_and_sorts(monkeypatch) -> None:
    os.environ["ECB_SERIES_KEY"] = "dummy"
    provider = EcbPortalProvider()

    payload = [
        {"FREQUENCY": "M", "PERIOD": "2026-02-01", "OBS_VALUE_AS_IS": "3.30"},
        {"FREQUENCY": "D", "PERIOD": "2026-02-02", "OBS_VALUE_AS_IS": "999"},
        {"FREQUENCY": "M", "PERIOD": "2026-01-01", "OBS_VALUE_AS_IS": "3.35"},
    ]

    def fake_fetch_observations(url: str, headers: dict, timeout: float):
        assert url.endswith("/data-detail-api/dummy")
        assert headers.get("Accept") == "application/json"
        assert timeout == 30.0
        return SimpleNamespace(raise_for_status=lambda: None, json=lambda: payload)

    monkeypatch.setattr(httpx, "get", fake_fetch_observations)

    observations = provider.fetch_observations()

    assert [(o.period_date, o.value) for o in observations] == [
        (date(2026, 1, 1), Decimal("3.35")),
        (date(2026, 2, 1), Decimal("3.30")),
    ]

