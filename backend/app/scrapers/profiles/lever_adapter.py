from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import httpx

from app.db.models.job_source import JobSource
from app.scrapers.contracts import ScrapedRecord, ScraperAdapterError


class LeverScraperAdapter:
    profile_code = "lever"

    def scrape(self, source: JobSource) -> list[ScrapedRecord]:
        config = source.config if isinstance(source.config, dict) else {}
        mode = str(config.get("mode", "fixture")).lower()

        if mode == "live":
            return self._scrape_live(source, config)
        return self._scrape_fixture(source, config)

    def _scrape_fixture(self, source: JobSource, config: dict[str, Any]) -> list[ScrapedRecord]:
        fixtures = config.get("fixtures")
        records = fixtures if isinstance(fixtures, list) else []

        now = datetime.now(timezone.utc)
        result: list[ScrapedRecord] = []
        for index, payload in enumerate(records):
            if not isinstance(payload, dict):
                continue
            external_ref = payload.get("id")
            result.append(
                ScrapedRecord(
                    external_ref=str(external_ref) if external_ref is not None else f"lv-{index}",
                    raw_payload=payload,
                    source_snapshot=None,
                    scraped_at=now,
                )
            )
        return result

    def _scrape_live(self, source: JobSource, config: dict[str, Any]) -> list[ScrapedRecord]:
        jobs_url = self._resolve_jobs_url(source, config)
        timeout_seconds = self._resolve_timeout(config)
        user_agent = self._resolve_user_agent(config)

        headers = {"Accept": "application/json", "User-Agent": user_agent}

        try:
            with httpx.Client(timeout=timeout_seconds, headers=headers, follow_redirects=True) as client:
                response = client.get(jobs_url)
                response.raise_for_status()
                payload = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise ScraperAdapterError(f"Lever live fetch failed for source {source.id}: {exc}") from exc

        jobs: list[dict[str, Any]]
        if isinstance(payload, list):
            jobs = [item for item in payload if isinstance(item, dict)]
        elif isinstance(payload, dict) and isinstance(payload.get("data"), list):
            jobs = [item for item in payload["data"] if isinstance(item, dict)]
        else:
            raise ScraperAdapterError(
                f"Lever live response format invalid for source {source.id}: expected list or object with 'data' list"
            )

        now = datetime.now(timezone.utc)
        result: list[ScrapedRecord] = []
        for index, job in enumerate(jobs):
            external_ref = job.get("id")
            result.append(
                ScrapedRecord(
                    external_ref=str(external_ref) if external_ref is not None else f"lv-live-{index}",
                    raw_payload=job,
                    source_snapshot=None,
                    scraped_at=now,
                )
            )
        return result

    @staticmethod
    def _resolve_jobs_url(source: JobSource, config: dict[str, Any]) -> str:
        url_value = config.get("jobs_url")
        if isinstance(url_value, str) and url_value.strip():
            return url_value.strip()
        raise ScraperAdapterError(
            f"Lever live mode requires 'jobs_url' in source config (source {source.id})"
        )

    @staticmethod
    def _resolve_timeout(config: dict[str, Any]) -> float:
        value = config.get("timeout_seconds", 10)
        if isinstance(value, (int, float)) and value > 0:
            return float(value)
        return 10.0

    @staticmethod
    def _resolve_user_agent(config: dict[str, Any]) -> str:
        value = config.get("user_agent")
        if isinstance(value, str) and value.strip():
            return value.strip()
        return "job-scraper-dashboard/1.0"
