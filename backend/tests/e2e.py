#!/usr/bin/env python3
import sys

import requests

BASE = "http://localhost:8080/api/v1"


def test_health() -> None:
    r = requests.get(f"{BASE}/health", timeout=10)
    assert r.status_code == 204, f"health: expected 204, got {r.status_code}"
    print("  GET /health → 204")


def test_ingest() -> None:
    r = requests.post(f"{BASE}/ingest", timeout=30)
    assert r.status_code == 200, f"ingest: expected 200, got {r.status_code} {r.text}"
    data = r.json()
    assert "ingested" in data, "ingest: missing ingested"
    assert isinstance(data["ingested"], int), "ingest: ingested is not int"
    assert data["ingested"] >= 0, "ingest: ingested should be >= 0"
    print(f"  POST /ingest → {data['ingested']}")


def test_observations() -> None:
    r = requests.get(
        f"{BASE}/observations",
        params={"start": "2022-01-01", "end": "2026-01-01"},
        timeout=30,
    )
    assert r.status_code == 200, f"observations: expected 200, got {r.status_code} {r.text}"
    data = r.json()
    assert isinstance(data, list), "observations: expected a list"
    assert len(data) > 0, "observations: expected non-empty list"
    first = data[0]
    assert "period_date" in first and "value" in first, "observations: missing fields"
    print(f"  GET /observations → {len(data)} rows")


def main() -> None:
    print(f"E2E tests → {BASE}")
    try:
        test_health()
        test_ingest()
        test_observations()
        print("E2E tests passed.")
    except AssertionError as e:
        print(f"E2E failed: {e}", file=sys.stderr)
        sys.exit(1)
    except requests.RequestException as e:
        print(f"E2E request error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

