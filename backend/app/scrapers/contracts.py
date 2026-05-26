from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from app.db.models.job_source import JobSource


class ScraperAdapterError(Exception):
    """Raised when adapter fetch/parse fails in live mode."""


@dataclass(slots=True)
class ScrapedRecord:
    external_ref: str | None
    raw_payload: dict[str, object]
    source_snapshot: str | None
    scraped_at: datetime


class ScraperAdapter(Protocol):
    profile_code: str

    def scrape(self, source: JobSource) -> list[ScrapedRecord]: ...
