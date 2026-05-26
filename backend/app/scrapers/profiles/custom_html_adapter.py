from __future__ import annotations

from datetime import datetime, timezone

from app.db.models.job_source import JobSource
from app.scrapers.contracts import ScrapedRecord


class CustomHtmlScraperAdapter:
    profile_code = "custom-html"

    def scrape(self, source: JobSource) -> list[ScrapedRecord]:
        fixtures = source.config.get("fixtures") if isinstance(source.config, dict) else None
        records = fixtures if isinstance(fixtures, list) else []

        now = datetime.now(timezone.utc)
        result: list[ScrapedRecord] = []
        for index, payload in enumerate(records):
            if not isinstance(payload, dict):
                continue
            external_ref = payload.get("id")
            snapshot = payload.get("snapshot")
            result.append(
                ScrapedRecord(
                    external_ref=str(external_ref) if external_ref is not None else f"ch-{index}",
                    raw_payload=payload,
                    source_snapshot=str(snapshot) if snapshot is not None else None,
                    scraped_at=now,
                )
            )
        return result
