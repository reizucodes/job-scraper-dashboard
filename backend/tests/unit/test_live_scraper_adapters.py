from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import httpx
import pytest

from app.db.models.job_source import JobSource
from app.scrapers.contracts import ScraperAdapterError
from app.scrapers.profiles.greenhouse_adapter import GreenhouseScraperAdapter
from app.scrapers.profiles.lever_adapter import LeverScraperAdapter


class FakeResponse:
    def __init__(self, payload: Any, status_code: int = 200) -> None:
        self._payload = payload
        self.status_code = status_code

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise httpx.HTTPStatusError(
                "HTTP error",
                request=httpx.Request("GET", "https://example.com"),
                response=httpx.Response(self.status_code),
            )

    def json(self) -> Any:
        return self._payload


class FakeClient:
    def __init__(self, *, payload: Any | None = None, exc: Exception | None = None, **_: Any) -> None:
        self._payload = payload
        self._exc = exc

    def __enter__(self) -> "FakeClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # type: ignore[no-untyped-def]
        return None

    def get(self, _: str) -> FakeResponse:
        if self._exc is not None:
            raise self._exc
        return FakeResponse(self._payload)


def _source(config: dict[str, Any]) -> JobSource:
    return JobSource(
        id=1,
        name="source",
        base_url="https://example.com",
        profile_id=1,
        enabled=True,
        config=config,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )


def test_greenhouse_live_mode_parses_jobs(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = {"jobs": [{"id": 11, "title": "Backend"}, {"id": 12, "title": "Frontend"}]}
    monkeypatch.setattr(httpx, "Client", lambda **kwargs: FakeClient(payload=payload, **kwargs))

    adapter = GreenhouseScraperAdapter()
    records = adapter.scrape(
        _source(
            {
                "mode": "live",
                "jobs_url": "https://boards-api.greenhouse.io/v1/boards/example/jobs?content=true",
            }
        )
    )

    assert len(records) == 2
    assert records[0].external_ref == "11"
    assert records[0].raw_payload["title"] == "Backend"


def test_lever_live_mode_parses_jobs_list(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = [{"id": "a1", "text": "Engineer"}, {"id": "a2", "text": "Manager"}]
    monkeypatch.setattr(httpx, "Client", lambda **kwargs: FakeClient(payload=payload, **kwargs))

    adapter = LeverScraperAdapter()
    records = adapter.scrape(
        _source(
            {
                "mode": "live",
                "jobs_url": "https://api.lever.co/v0/postings/example?mode=json",
            }
        )
    )

    assert len(records) == 2
    assert records[1].external_ref == "a2"
    assert records[1].raw_payload["text"] == "Manager"


def test_live_mode_timeout_raises_adapter_error(monkeypatch: pytest.MonkeyPatch) -> None:
    timeout_exc = httpx.ReadTimeout("timeout", request=httpx.Request("GET", "https://example.com"))
    monkeypatch.setattr(httpx, "Client", lambda **kwargs: FakeClient(exc=timeout_exc, **kwargs))

    adapter = GreenhouseScraperAdapter()
    with pytest.raises(ScraperAdapterError):
        adapter.scrape(_source({"mode": "live", "jobs_url": "https://boards-api.greenhouse.io/v1/boards/example/jobs"}))


def test_fixture_mode_unchanged() -> None:
    adapter = LeverScraperAdapter()
    records = adapter.scrape(_source({"fixtures": [{"id": "fixture-1", "text": "Fixture Job"}]}))

    assert len(records) == 1
    assert records[0].external_ref == "fixture-1"
